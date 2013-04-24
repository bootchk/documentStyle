'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

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
  def __init__(self, name, selector):
    '''
    Responsibility: know name
    '''
    assert name is not None
    self.name = name
    self.selector = selector # immutable
  
  
  def __repr__(self):
    return self.name +"[" +  ",".join( map( str, self) ) + "]"
                     
                      
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
      if selector.matches(formation.selector):
        styleProperty = formation.selectStyleProperty(selector)
        if styleProperty is not None:
          return styleProperty
    return None
    

  
  def display(self, top=False):
    '''
    Responsibility: Display for editing in tree like form.
    '''
    return FormationLayout(self, top)
  

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
        stylingAct = StylingAct(item.selector, item.get())
        derivingStylingActSet.put(stylingAct)
      elif item.wasReset():
        # property was not inherited (overridden), but was reinherited.  StylingAct revoked.
        derivingStylingActSet.delete(item.selector)
      # else item isReset, was inherited, and still inherited.  No StylingAct
        
  
  #@report
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
    
    
