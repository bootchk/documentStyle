'''
'''
from PySide.QtCore import Qt
from PySide.QtGui import QPen

from documentStyle.styleWrapper.styleWrapper import PenStyleWrapper


class AdaptedPenModel(object):
  '''
  Mimics a PySide enum: "values" attribute is a dictionary.
  But uses a pickleable type 
  (PySide Qt enum not pickleable since enum values are class attributes.)
  
  Responsibility:
  - standard dictionary responsibilities
  - know default value from model
  '''
  
  def __init__(self):
    self.values = {"None": PenStyleWrapper(Qt.PenStyle.NoPen),
                   "Solid": PenStyleWrapper(Qt.PenStyle.SolidLine),
                   "Dashed": PenStyleWrapper(Qt.PenStyle.DashLine),
                   "Dotted": PenStyleWrapper(Qt.PenStyle.DotLine),
                   "DashDot": PenStyleWrapper(Qt.PenStyle.DashDotLine),
                   }
    
    # TODO more values Qt::DashDotDotLine  Qt::CustomDashLine
  
  
  def default(self):
    ''' Framework defined default, from a new pen. '''
    return PenStyleWrapper(QPen().style())


PenModel = AdaptedPenModel()