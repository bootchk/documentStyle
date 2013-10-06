'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtWidgets import QLabel

from documentStyle.userInterface.form.formationForm import FormationForm
from documentStyle.userInterface.layout.formationLayout import FormationLayout
from documentStyle.styling.stylingAct import StylingAct

from documentStyle.debugDecorator import report


class Formation(list):
  '''
  Defines how something draws (appears.)
  
  A Formation is applied to an Instrument, which is applied to a Document Element.
  Here, and in Qt, these applies are copies of the attributes of the Formation.
  That is, Formation attributes applied to an Instrument are copies,
  and Instrument attributes applied to a DocumentElement are copies
  (The Formation and Instrument itself are not copied, it is a stamping process.)
  
  Composite via inherit List.
  
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
  - select styleProperty from self
  - display for editing
  - persist (as attached to styled morphs of a document)
  
  '''
  def __init__(self, name, selector, role=""):
    '''
    Responsibility: know name
    '''
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
  
  
  def __repr__(self):
    ''' Self is List. list.repr() is verbose. '''
    return self.name  # short
    
    
  def _longRepr(self): 
    '''
    list.repr() would be on one line.  Reformat to indented multi-line, for debugging.
    '''
    return self.name +"[" +  ",\n       ".join( map( str, self) ) + "]\n"
          
            
                      
  @report
  def applyTo(self, morph):
    '''
    Responsibility: apply self to morph.
    
    Apply all contained Formations to morph.
    '''
    for formation in self:
      formation.applyTo(morph)
    
  
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
      for formation in self:
        if formation.name == selector.DEType:
          result = formation
          break
    else:
      assert selector.DEType == "*"
      # All children match, return composite
      result = Formation("subFormation", selector)
      for formation in self:
        result.append(formation)
    return result
    
  
  def selectStyleProperty(self, selector):
    '''
    Select (by selector) a styleProperty.
    
    May return None.
    '''
    for formation in self:
      # Recurse into child Formations
      if selector.matches(formation.selector):
        styleProperty = formation.selectStyleProperty(selector)
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
    for formation in self:
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
    '''
    #print "reflectToStylingActSet", derivingStylingActSet

    for item in self.generateStyleProperties():
      if not item.isReset():
        ''' 
        User edited (in-lined.)  Create or replace styling act.
        '''
        stylingAct = StylingAct(item.selector, item.get())
        #print "New styling act"
        derivingStylingActSet.put(stylingAct)
      else:
        '''
        Reset to inherited value.  Delete any previous styling act.
        
        TODO optimization to avoid needless try delete:
        If item.wasInitiallyReset: i.e. not in-lined
          pass
        else:
          # assert StylingAct exists
          derivingStylingActSet.delete(item.selector)
        '''
        derivingStylingActSet.deleteIfExists(item.selector)
      
      
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
    
  
  def generateStyleProperties(self):
    '''
    Recursive generator.
    Partially deferred (terminal in InstrumentFormation)
    '''
    for formation in self:
      for styleProperty in formation.generateStyleProperties():
        yield styleProperty
    
    
