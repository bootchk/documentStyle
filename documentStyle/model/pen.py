'''
'''
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPen

#from documentStyle.styleWrapper.styleWrapper import PenStyleWrapper


class AdaptedPenModel(object):
  '''
  Mimics a PyQt4 enum: "values" attribute is a dictionary.
  But uses a pickleable type 
  (PyQt4 Qt enum not pickleable since enum values are class attributes.)
  
  Responsibility:
  - standard dictionary responsibilities
  - know default value from model
  '''
  
  def __init__(self):
    qtEnum = Qt # PySide qtEnum = Qt.PenStyle
    """
    PySide
    self.values = {"None": PenStyleWrapper(qtEnum.NoPen),
                   "Solid": PenStyleWrapper(qtEnum.SolidLine),
                   "Dashed": PenStyleWrapper(qtEnum.DashLine),
                   "Dotted": PenStyleWrapper(qtEnum.DotLine),
                   "DashDot": PenStyleWrapper(qtEnum.DashDotLine),
                   }
    """
    self.values = {"None": qtEnum.NoPen,
                   "Solid": qtEnum.SolidLine,
                   "Dashed": qtEnum.DashLine,
                   "Dotted": qtEnum.DotLine,
                   "DashDot": qtEnum.DashDotLine,
                   }
    
    # TODO more values Qt::DashDotDotLine  Qt::CustomDashLine
  
  
  def default(self):
    ''' Framework defined default, from a new pen. '''
    #return PenStyleWrapper(QPen().style())
    return QPen().style()



PenModel = AdaptedPenModel()