'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

'''
see instrument.py

Wrap a Qt Instrument.
'''
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextBlockFormat


class BlockInstrument(QTextBlockFormat):
  '''
  Contain block parameters.
  '''
  def __init__(self):
    super().__init__()
    # These should be the same as framework's default
    self.defaultAligning = 0  # Left
    self.defaultSpacing = 0   # Single
    # Cache
    self._alignment = 0
    self._spacing = 0
    
    self._adaptInitialInstrument()
    
    
  def _adaptInitialInstrument(self):
    '''
    Ensure instrument is initted with our defaults.
    '''
    '''
    !!! QTextBlockFormat.lineHeight() defaults to value 0 for 'single spacing.'  
    Set the default according to lineHeightType=proportional.
    I.E. this changes super.lineHeightType and sets it.
    '''
    self.setSpacing(0)
    assert super().lineHeight() == 100
    
    '''
    
    '''
    self.setAlignment(0)
    assert super().alignment() == Qt.AlignLeft
    

  '''
  Aligning
  '''
  def setAlignment(self, value):
    '''
    Adapt view model to Qt instrument model.
    '''
    adaptedValue = self._adaptAlignment(value)
    super().setAlignment(adaptedValue)
    self._alignment = value
    
    
  def alignment(self):
    '''
    We don't unadapt, just return cached value.
    '''
    return self._alignment
  


  '''
  Spacing
  '''
  def setSpacing(self, value):
    '''
    Adapt view model to Qt instrument model.
    '''
    adaptedValue = self._adaptLineSpacing(value)
    super().setLineHeight(adaptedValue, QTextBlockFormat.ProportionalHeight)
    self._spacing = value
    
    
  def spacing(self):
    return self._spacing
        
        
  '''
  Adapt our model (a continguous enum) to/from Qt's instrument model.
  '''
  def _adaptLineSpacing(self, value):
    '''
    Adapt model to instrument setter, which takes two parameters.
    Always lineHeightType=proportional, values always percent e.g. 100, 150, 200
    '''
    assert value >= 0 and value < 3
    if value == 0:
      result = 100
    elif value == 1:
      result = 200
    elif value == 2:
      result = 150
    assert result in (100, 150, 200)
    return result
    
    
    
  def _adaptAlignment(self, value):
    '''
    Adapt model to instrument setter, which takes a Qt.Alignment flag having values 1,2,4,8
    '''
    assert value >=0 and value < 4
    if value == 0:
      result = Qt.AlignLeft
    elif value == 1:
      result = Qt.AlignRight
    elif value == 2:  # !!!! Horizontal
      result = Qt.AlignHCenter
    elif value == 3:
      result = Qt.AlignJustify
    else:
      print("Unknown alignment value")
      result = Qt.AlignLeft # defaults to some valid value
    return result
  
  """
  OLD
    '''
    Convert int to Qt.Alignment type
    Solves problem in QML that I don't fully understand.
    Note below that Python doesn't care about the comparison types,
    but PyQt gives TypeError if use unadapted value of type int.
    
    Possibly we could also fix by defining ResettableAlignmentValue of type QtCore.Alignment ?
    '''
    assert value > 0, "Zero is not a proper flag."
    
    if value == Qt.AlignLeft:
      adaptedValue = Qt.AlignLeft
    elif value == Qt.AlignRight:
      adaptedValue = Qt.AlignRight
    elif value == Qt.AlignHCenter:  # !!!! Horizontal
      adaptedValue = Qt.AlignHCenter
    elif value == Qt.AlignJustify:
      adaptedValue = Qt.AlignJustify
    else:
      print("Unknown alignment value")
      adaptedValue = Qt.AlignLeft # defaults to some valid value
    print("adaptAlignment called", adaptedValue)
    self.instrument.setAlignment(adaptedValue)
  """