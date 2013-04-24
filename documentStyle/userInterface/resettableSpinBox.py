'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import Qt
from PySide.QtGui import QSpinBox
from resettable import Resettable


class ResettableSpinBox(Resettable, QSpinBox):
  
  def __init__(self, resettableValue):
    QSpinBox.__init__(self)
    Resettable.__init__(self, resettableValue)
    
    self.setAlignment(Qt.AlignRight)