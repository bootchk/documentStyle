
from .textFormation import TextFormation
from documentStyle.instrument.charInstrument import CharInstrument
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation

from documentStyle.styleProperty.styleProperty import BaseStyleProperty
from documentStyle.styleProperty.stylePropertyFont import FontStyleProperty
from documentStyle.styleProperty.resettableValue import ResettableColorValue, ResettableFontValue
from documentStyle.ui.layout.typedStylePropertyLayout import ColorStylePropertyLayout, FontStylePropertyLayout



class CharacterFormation(TextFormation):
  '''
  Styling attributes of characters.
  
  Specialize to Qt <QTextCharFormat>
  
  Notes:
  Color property is foreground.
  We choose not to offer background color as a style property.
  Background color applied to text document gives jaggy blocks of color background.
  Probably better to offer a property on a background layer (symmetric balloon) behind the text. 
  Background color defaults to transparent.
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name='Character', parentSelector=parentSelector)
    self.instrument = CharInstrument()
    self.styleProperties=[BaseStyleProperty('Color', self.instrument.setForegroundColor, self.selector,
                                             resettableValueFactory=ResettableColorValue,
                                             layoutFactory=ColorStylePropertyLayout,
                                             default=self.instrument.defaultColor, ),
                          FontStyleProperty('Font', self.instrument.setFont, self.selector,
                                        resettableValueFactory=ResettableFontValue,
                                        layoutFactory=FontStylePropertyLayout,
                                        # This value is QFont, not pickleable. FontStyleProperty wraps it.
                                        default=self.instrument.defaultFont, ), 
                          ]
                                        ## model = FontModel),]

  
  def applyToCursor(self, cursor):
    ''' 
    Effect deferred method. 
    
    !!! Must be setCharFormat, not mergeCharFormat.
    Merge seems to mean: only set properties that program touched in the Format.
    We don't touch them all, so for a merge, Qt will not set them all.
    Yet for a reset, we need the defaulted properties to be set on cursor.
    '''
    cursor.setCharFormat(self.instrument)

    
    
    
  
    
