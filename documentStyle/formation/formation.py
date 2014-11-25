'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from documentStyle.userInterface.form.formationForm import FormationForm
#from documentStyle.userInterface.layout.formationLayout import FormationLayout
from documentStyle.styling.stylingAct import StylingAct

from documentStyle.debugDecorator import report, reportTrueReturn


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
    return self.name + ':' + str(self.selector)  # short
    
    
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
    
  
  def selectStyleProperty(self, selectorOfStylingAct):
    '''
    First styleProperty selected by selectorOfStylingAct, or None.
    Depends on styleProperties in order of selectivity (more selective, i.e. specific, last.)
    '''
    for childFormation in self:
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
      #print("item.isReset is true")
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
    
  
  def generateStyleProperties(self):
    '''
    Recursive generator.
    Partially deferred (terminal in InstrumentFormation)
    '''
    for formation in self:
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
        break 
    return result
    
