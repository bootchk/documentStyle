'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import QObject, pyqtSlot

from documentStyle.userInterface.form.formationForm import FormationForm
#from documentStyle.userInterface.layout.formationLayout import FormationLayout
from documentStyle.styling.stylingAct import StylingAct
from documentStyle.selector import Selector
from documentStyle.styleProperty.resettableValue import BaseResettableValue

from documentStyle.debugDecorator import report, reportTrueReturn


class Formation(QObject):
  '''
  Defines how something draws (appears.)
  
  Also, a model for a GUI to edit a stylesheet (for QML GUI.)
  
  A Formation is applied to an Instrument, which is applied to a Document Element.
  Here, and in Qt, these applies are copies of the attributes of the Formation.
  That is, Formation attributes applied to an Instrument are copies,
  and Instrument attributes applied to a DocumentElement are copies
  (The Formation and Instrument itself are not copied, it is a stamping process.)
  
  Has-a List (formerly is-a List.)  Now a QObject so that can be exposed to QML.
  
  Called a Formation (not Format): is a noun, and distinguishes from Qt Q...Format.
  
  Abstract.
  
  Similar to QStyleOption: a simple set of parameters.
  Unlike QStyleOption, which Style functions read,
  a Formation applies itself to a Styleable object.
  
  Can be attached to DocumentElements and persisted (template styling)
  OR can be computed on the fly from cascading StyleSheets (if stylesheets persist, no need for Formations to persist.)
  
  Responsibilities:
  - know name
  - know selector
  - apply to morph
  - selectable (styleProperty and their resettableValue) by Selector or dotted string
  - display for editing
  - persist (as attached to styled morphs of a document)
  - reflect to StylingActSet
  - iterable over subformations (top) and styleProperties (leaves)
  
  selection of resettableValues of stylingProperties by dotted string name is for QML
  '''
  def __init__(self, name, selector, role=""):
    '''
    Responsibility: know name
    '''
    super().__init__()  # init QObject
    assert name is not None
    self.name = name
    self.selector = selector # immutable
    '''
    role this formation plays in styling an element.
    The same formation type can play many roles in styling a composite document element.
    E.G. a PenFormation can play role "Frame " styler and also "Interior" styler.
    Or it may not be obvious to user what role a Formation (usually InstrumentFormation) plays,
    e.g. what role does a Pen play on Text: style the chars or style the frame?
    Usually role is obvious, i.e. role of a Pen on a Line is to style the line.
    '''
    self.role = role
    self.subFormations = []
  
  
  def __repr__(self):
    ''' Self is List. list.repr() is verbose. '''
    return self.name + ':' + str(self.selector)  # short
    
    
  def _longRepr(self): 
    '''
    list.repr() would be on one line.  Reformat to indented multi-line, for debugging.
    '''
    return self.name +"[" +  ",\n       ".join( map( str, self) ) + "]\n"
          
          
  '''
  List-like.  Delegate to owned list.
  len, append, and iterable
  '''
  def __len__(self):
    return len(self.subFormations)
  
  def append(self, value):
      self.subFormations.append(value)
      
      
                      
  @report
  def applyTo(self, morph):
    '''
    Responsibility: apply self to morph.
    
    Apply all contained Formations to morph.
    '''
    for formation in self.subFormations:
      formation.applyTo(morph)
    
  '''
  Responsibility: expose self to QML as a model
  '''
  def exposeToQML(self, view):
    assert view is not None # created earlier
    view.rootContext().setContextProperty('stylesheetModel', self)
    print("After setContextProperty")
    
  
  @pyqtSlot(str, result=BaseResettableValue)
  def selectResettableValueByStringSelector(self, string):
    '''
    Slot for use by QML.
    Formation is a model, QML selects resettable values by dotted string name.
    '''
    selector = Selector.fromString(string)
    styleProperty = self.selectStyleProperty(selector)
    assert styleProperty is not None
    result = styleProperty.resettableValue
    # assert isintance(result, BaseResettableValue) but polymorphic, a subclass
    return result
  
  
      
  '''
  Responsibility: Selectable
  '''
  
  def selectSubformation(self, selector):
    '''
    Formation comprising all child Formations that match selector,
    or a single child Formation.
    Ensure that result root does not have a single child (not single trunked tree.)
    
    This only works for DEType, and won't work for (..., DEType, instrument, ...) i.e. does not recurse.
    This is not general, but specific to DEType.
    '''
    # TODO need to return a copy of child formations???
    #print "selectSubformation, selector is ", selector
    
    if selector.isDETypeSelector():
      for formation in self.subFormations:
        if formation.name == selector.DEType:
          result = formation
          break
    else:
      assert selector.DEType == "*"
      # All children match, return composite
      result = Formation("subFormation", selector)
      for formation in self.subFormations:
        result.append(formation)
    
    assert result is not None, "No match, selector is ill-formed. "
    return result
  
    
  def selectStyleProperty(self, selectorOfStylingAct):
    '''
    First styleProperty selected by selectorOfStylingAct, or None.
    Depends on styleProperties in order of selectivity (more selective, i.e. specific, last.)
    '''
    for childFormation in self.subFormations:
      '''
      childFormation.selector is NOT necessarily more selective than selectorOfStylingAct
      E.G. childFormation (*,Line,*,*) is not more selective than selectorOfStylingAct(*,*,Pen,Color) 
      '''
      ##ORG if childFormation.selector.matches(selectorOfStylingAct):
      ## if selectorOfStylingAct.matches(childFormation.selector):
      ## if selectorOfStylingAct.commutativeMatches(childFormation.selector):
      if selectorOfStylingAct.matchesToInstrument(childFormation.selector):
        styleProperty = childFormation.selectStyleProperty(selectorOfStylingAct) # recursion
        if styleProperty is not None:
          return styleProperty
    return None
    

  '''
  Display (GUI editing.)
  '''
  
  def display(self, top=False):
    '''
    Responsibility: Display for editing in list like form (indented tree)
    See also: StyleProperty.display()
    
    Returns QWidget (QLayout or QFormLayout)
    '''
    # This ALTERNATIVE creates a QFormLayout
    return FormationForm(formation=self, top=top)
    # This ALTERNATIVE creates a QGridLayout
    #return FormationLayout(formation=self, top=top)
    
    

  '''
  Layout editing.
  '''
  def displayContentsInLayout(self, layout):
    '''
    Tree structured layout into given layout.
    '''
    for formation in self.subFormations:
      # Indirect recursion through display() which eventually calls displayContentsInLayout again
      layout.addLayout(formation.display())
  
  
  def isSingleValued(self):
    ''' 
    Base.  Redefined by terminal subclasses. 
    Single valued Formation displays in a row instead of a table.
    '''
    return len(self) < 2
  
  
  
  
  @report
  def reflectToStylingActSet(self, derivingStylingActSet):
    '''
    Reflect user's changes into a derivingStylingActSet.
    
    Self was derived through derivingStylingActSet.  
    Update it with user's changes.
    
    For debugging, return count of StylingActs deleted.
    '''
    #print "reflectToStylingActSet", derivingStylingActSet
    deletedCount = 0
    for item in self.generateStyleProperties():
      if item.resettableValue.touched:  # WAS not item.isReset():
        #print('touched')
        if self.reflectItemToStylingAct(item, derivingStylingActSet):
          deletedCount += 1
    return deletedCount
  
      
  def reflectItemToStylingAct(self, item, derivingStylingActSet):
    '''
    Item was touched by user.  Create, update, or delete styling act.
    
    Return True if delete
    '''
    if item.resettableValue.isReset:
      '''
      User touched (one or more changes) but last act was to Reset to inherited value.
      Delete any previous styling act. (If initially reset, then user touched, then reset, no styling act exists.)
      '''
      print("item.isReset is true")
      result = derivingStylingActSet.deleteIfExists(item.selector)
    else:
      ''' 
      User edited (in-lined.)  Create or replace styling act.
      '''
      stylingAct = StylingAct(item.selector, item.get())
      #print("New styling act", stylingAct)
      derivingStylingActSet.put(stylingAct)
      result = False
    return result
      
      
    """
    OLD
    if not item.isReset():
      '''
      property was inherited, but was overridden.  StylingAct will be new.
      OR property was not inherited, but might have been changed.  StylingAct will be updated.
      '''
      stylingAct = StylingAct(item.selector, item.get())
      derivingStylingActSet.put(stylingAct)
    elif item.wasReset():
      # property was not inherited (overridden), but was reinherited.  StylingAct revoked.
      derivingStylingActSet.delete(item.selector)
    # else item isReset, was inherited, and still inherited.  No StylingAct
    """
        
  
  @report
  def rollStyleProperties(self):
    '''
    Roll forward all styleProperty, meaning: not overridden by subsequent (in cascade) inline StylingAct.
    That is, when cascading, non-inherited value at one level becomes inherited again at next level.
    If user chooses "Inherit" button, it inherits only from original value from previous cascade,
    not all the way back to the App StyleSheet original values.
    '''
    for item in self.generateStyleProperties():
      item.roll()
    
  '''
  Iterable
  '''
  def generateSubformations(self):
    '''
    Generate my direct children
    '''
    for subformation in self.subFormations:
      yield subformation
      
        
  def generateStyleProperties(self):
    '''
    Generate leaves.
    Recursive: subformations in turn generateStyleProperties
    Partially deferred (terminal in InstrumentFormation)
    '''
    for formation in self.subFormations:
      for styleProperty in formation.generateStyleProperties():
        yield styleProperty
  
  """
  @reportTrueReturn
  def isEdited(self):
    '''
    Are any of my properties not reset?
    I.E. are any of my properties edited (at some time in the past.)
    '''
    result = False
    for item in self.generateStyleProperties():
      print("isEdited", item)
      if not item.isReset:
        result = True
    return result
  """
    
  
  @reportTrueReturn
  def isTouched(self):
    ''' Composite: Are any of my properties touched? Since formation was created for editing. '''
    result = False
    for item in self.generateStyleProperties():
      if item.resettableValue.touched:
        result = True
        print("StyleProperty was touched", item)
        break 
    return result
    
    
  
