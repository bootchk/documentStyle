'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDoubleSpinBox
from .resettable import Resettable


class ResettableDoubleSpinBox(Resettable, QDoubleSpinBox):
  
  def __init__(self, resettableValue):
    QDoubleSpinBox.__init__(self)
    Resettable.__init__(self, resettableValue)
    
    self.setAlignment(Qt.AlignRight)