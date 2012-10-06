'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from ..selector import DETypeSelector
from formation import Formation
from instrumentFormation.penFormation import PenFormation
from instrumentFormation.brushFormation import BrushFormation
from instrumentFormation.characterFormation import CharacterFormation
from instrumentFormation.blockFormation import BlockFormation
from instrumentFormation.opacityFormation import OpacityFormation
from instrumentFormation.graphicEffectFormation import GraphicEffectFormation



class MorphFormation(Formation):
  '''
  Composite of InstrumentFormation.
  
  Configurer: of the set of InstrumentFormation appropriate for a DocumentElement (Morph).
  
  Declares the "tools" e.g. brush, that a user thinks of (models) as drawing a DocumentElement.
  The framework supports the same model, and this has little fix for any mismatch of the models.
  
  Abstract.
  '''
  def __init__(self, name):
    Formation.__init__(self, name, selector=DETypeSelector(name))
    



class LineFormation(MorphFormation):
  '''  <Line> style configuration. '''
  
  def __init__(self):
    MorphFormation.__init__(self, "Line")
    self.append(PenFormation(parentSelector=self.selector()))
    self.append(OpacityFormation(parentSelector=self.selector()))



class ShapeFormation(MorphFormation):
  ''' <Shape> style configuration  '''
  
  def __init__(self):
    MorphFormation.__init__(self, "Shape")
    self.append(PenFormation(parentSelector=self.selector()))
    self.append(BrushFormation(parentSelector=self.selector()))
    self.append(OpacityFormation(parentSelector=self.selector()))
    
    
    
class TextFormation(MorphFormation):
  ''' <Text> style configuration '''
  
  def __init__(self):
    MorphFormation.__init__(self, "Text")
    self.append(CharacterFormation(parentSelector=self.selector()))
    self.append(BlockFormation(parentSelector=self.selector()))
    self.append(OpacityFormation(parentSelector=self.selector()))
    


class PixmapFormation(MorphFormation):
  '''
  <Pixmap> style configuration.
  
  Terminology: the Formation of an image is the styling formation, not the format, i.e. encoding e.g. PNG.
  '''
  
  def __init__(self):
    MorphFormation.__init__(self, "Pixmap")
    self.append(OpacityFormation(parentSelector=self.selector()))
    self.append(GraphicEffectFormation(parentSelector=self.selector()))


    
    