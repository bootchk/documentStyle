'''
'''

from PySide.QtCore import Qt


class AdaptedBrushModel(object):
  '''
  Mimics a PySide enum: has "values" attribute that is a dictionary
  '''
  def __init__(self):
    self.values = {"None": Qt.BrushStyle.NoBrush,
                   "Solid": Qt.BrushStyle.SolidPattern }
    # TODO more values
  

BrushModel = AdaptedBrushModel()