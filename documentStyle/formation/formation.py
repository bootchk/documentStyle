'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from documentStyle.userInterface.layout.formationLayout import FormationLayout
from documentStyle.styling.stylingAct import StylingAct

class Formation(list):
  '''
  Defines how something draws (appears.)
  
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
  def __init__(self, name, selector):
    '''
    Responsibility: know name
    '''
    assert name is not None
    self.name = name
    self._selector = selector # immutable
  
  
  def __repr__(self):
    return self.name +"[" +  ",".join( map( str, self) ) + "]"
  
  
  def selector(self):
    ''' Responsibility: know selector. '''
    return self._selector
                     
                      
  def applyTo(self, morph):
    '''
    Responsibility: apply self to morph.
    
    Apply all contained Formations to morph.
    '''
    for formation in self:
      print "Formation.applyTo", formation
      formation.applyTo(morph)
    
  
  def selectSubformation(self, selector):
    '''
    Select (by selector) a sub formation.
    Returns Formation comprising all child Formations that match selector.
    
    This only works for DEType, and won't work for (..., DEType, instrument, ...)
    i.e. does not recurse
    '''
    # TODO need to return a copy of child formations???
    # print "selectSubformation, selector is ", selector
    subFormation = Formation("subFormation", selector)
    for formation in self:
      if formation.name == selector.DEType or selector.DEType == "*":
        subFormation.append(formation)
    return subFormation
    
  
  def selectStyleProperty(self, selector):
    '''
    Select (by selector) a styleProperty.
    
    May return None.
    '''
    for formation in self:
      # Recurse into child Formations
      if selector.matches(formation.selector()):
        styleProperty = formation.selectStyleProperty(selector)
        if styleProperty is not None:
          return styleProperty
    return None
    

  
  def display(self):
    '''
    Responsibility: Display for editing in tree like form.
    '''
    return FormationLayout(self)
  

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
        property was inherited, but was overridden.  StylingAct will be new.
        OR property was not inherited, but might have been changed.  StylingAct will be updated.
        '''
        stylingAct = StylingAct(item.selector(), item.get())
        derivingStylingActSet.put(stylingAct)
      elif item.wasReset():
        # property was not inherited (overridden), but was reinherited.  StylingAct revoked.
        derivingStylingActSet.delete(item.selector())
      # else item isReset, was inherited, and still inherited.  No StylingAct
        
  
  def resetResettableStyleProperties(self):
    '''
    Reset user's changes.
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
    
    
