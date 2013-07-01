'''
'''

from PySide.QtCore import Qt


class AdaptedAlignmentModel(object):
  '''
  Mimics a PySide enum: has "values" attribute that is a dictionary
  
  Here, we limit to one dimension (horizontal) of two dimensional alignment
  '''
  def __init__(self):
    self.values = {"Left": Qt.AlignmentFlag.AlignLeft,
                   "Right": Qt.AlignmentFlag.AlignRight,
                  "Center": Qt.AlignmentFlag.AlignHCenter,
                  "Justify": Qt.AlignmentFlag.AlignJustify,}
    # TODO more values

AlignmentModel = AdaptedAlignmentModel()