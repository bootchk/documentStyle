'''
'''
from documentStyle.selector import instrumentSelector
from documentStyle.formation.formation import Formation



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
  - base: the underlying object from GUI framework that styles an instrument
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
  
  def __init__(self, name, parentSelector):
    Formation.__init__(self, name, selector=instrumentSelector(parentSelector, name))
  
  
  def __repr__(self):
    return self.name +"[" +  ",".join( map( str, self.styleProperties) ) + "]"
    
    
  def isSingleValued(self):
    ''' Effect a deferred method. '''
    return len(self.styleProperties) < 2
  
  
  def selectStyleProperty(self, selector):
    '''
    Return styleProperty selected by selector or None.
    
    Redefines the composite recursive method, to be terminal.
    '''
    '''
    Could use: if selector.matches(self.selector())
    As an optimization, assert prefix of selector matches, and only check the suffix.
    '''
    result = None
    for styleProperty in self.styleProperties:
      if styleProperty.name == selector.field or selector.field == "*":
        result = styleProperty
    #print "selectStyleProperty returns", self.name, result
    return result


  def displayContentsInLayout(self, layout):
    '''
    Redefines.
    For this terminal Formation (without child Formations), 
    display StyleProperty layout/widgets, not layouts of child Formations.
    '''
    for p in self.styleProperties:
      layout.addLayout(p.layout())


  def generateStyleProperties(self):
    '''
    Redefines to be terminal (non-recursing.)
    '''
    for item in self.styleProperties:
      yield item
  

  def applyTo(self):
    raise "NotImplementedError" # deferred
  




