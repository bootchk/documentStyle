'''
'''
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

import documentStyle.config as config
#from documentStyle.styleWrapper.styleWrapper import PenStyleWrapper


class AdaptedPenModel(object):
  '''
  Mimics a PyQt5 enum: "values" attribute is a dictionary.
  But uses a pickleable type 
  (PyQt5 Qt enum not pickleable since enum values are class attributes.)
  
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
    self.values = {config.i18ns.NoneName : qtEnum.NoPen,
                   config.i18ns.Solid : qtEnum.SolidLine,
                   config.i18ns.Dashed : qtEnum.DashLine,
                   config.i18ns.Dotted : qtEnum.DotLine,
                   config.i18ns.DashDot : qtEnum.DashDotLine,
                   }
    
    # TODO more values Qt::DashDotDotLine  Qt::CustomDashLine
  
  
  def default(self):
    ''' Framework defined default, from a new pen. '''
    #return PenStyleWrapper(QPen().style())
    return QPen().style()
