'''
'''

from documentStyle.selector import instrumentSelector
from documentStyle.formation.formation import Formation

from documentStyle.debugDecorator import reportNotNoneReturn



class InstrumentFormation(Formation):
  '''
  Set of StyleProperty for a graphical instrument:
  - brush
  - pen
  - text renderer
  -- char
  -- block
  - thinner (opacity)
  - graphicaleffector (effects or filters)
  
  A primitive or terminal Formation: contains no further Formations.
  But it does have a length, the count of StyleProperties.
  
  Abstract.
  
  Deferred attributes:
  - instrument: the underlying object from GUI framework that carries style to a drawable
  - name: the name of instrument, used in selectors
  - styleProperties: list of elemental properties
  
  The __init__ method of subclasses configures deferred attributes.
  Especially the set of StyleProperty.
  The configured set may differ from the set supported by the framework.
  In other words, only expose a subset of the set supported by framework.
  
  Initial (default) values of Formation's StyleProperty are AS DEFINED BY GRAPHICS FRAMEWORK, not as defined by app.
  Values displayed may be values previously chosen by user (and stored in Formation.)
  
  Certain formations have only one StyleProperty and apply to a whole DocumentElement. E.G. Opacity.
  The only behavioral difference from Formations that have many StyleProperty is how they are displayed
  (the latter have subheadings e.g. "Line".)
  '''
  
  def __init__(self, name, parentSelector, role=""):
    Formation.__init__(self, name, selector=instrumentSelector(parentSelector, name), role=role)
  
  
  def __repr__(self):
    return self.name +"[" +  ",".join( map( str, self.styleProperties) ) + "]"
    
    
  def isSingleValued(self):
    ''' Effect a deferred method. '''
    return len(self.styleProperties) < 2
  
  @reportNotNoneReturn
  def selectStyleProperty(self, selectorOfStylingAct):
    '''
    See formation.selectStyleProperty() which is recursive to here.
    
    Redefines the composite recursive method, to be terminal.
    '''
    result = None
    for styleProperty in self.styleProperties:
      '''
      assert prefix of selectorOfStylingAct matches this instrumentFormation, and only check the suffix.
      '''
      ## Name not implemented: assert styleProperty.selector.name == selectorOfStylingAct.name
      assert styleProperty.selector.DEType == selectorOfStylingAct.DEType or selectorOfStylingAct.DEType == '*'
      assert selectorOfStylingAct.field != "*"
      if styleProperty.name == selectorOfStylingAct.field:
        result = styleProperty
      """
      Alternative 2
      
      if selectorOfStylingAct.noncommutativeMatches(styleProperty.selector):
        print(">>>>> matching styleProperty selector", styleProperty.selector)
        result = styleProperty
      """
    #print("instrumentFormation.selectStyleProperty returns", self.name, result)
    return result


  def displayContentsInLayout(self, parentLayout):
    '''
    Reimplements.
    For this terminal Formation (without child Formations), 
    display StyleProperty layout/widgets, not layouts of child Formations.
    '''
    for p in self.styleProperties:
      parentLayout.addLayout(p.getLayout(isLabeled=True))


  def generateStyleProperties(self):
    '''
    Redefines to be terminal (non-recursing.)
    '''
    for item in self.styleProperties:
      yield item
  

  def applyValuesToInstrument(self):
    '''
    Instrument is defaulted by framework (NOT same values as held by this Formation) until either:
    - edited
    - call applyValuesToInstrument
    
    Currently not used???
    '''
    for item in self.styleProperties:
      item.applyValueToInstrument()
    
    
  def applyTo(self):
    ''' Apply my instrument to DocumentElement. '''
    raise NotImplementedError('Deferred')
  




