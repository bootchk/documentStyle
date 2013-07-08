'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import Qt

from documentStyle.styleWrapper.styleWrapper import AlignmentStyleWrapper


class AdaptedAlignmentModel(object):
  '''
  Mimics a PySide enum: has "values" attribute that is a dictionary
  
  Here, we limit to one dimension (horizontal) of two dimensional alignment
  '''
  def __init__(self):
    self.values = {"Left": AlignmentStyleWrapper(Qt.AlignmentFlag.AlignLeft),
                   "Right": AlignmentStyleWrapper(Qt.AlignmentFlag.AlignRight),
                  "Center": AlignmentStyleWrapper(Qt.AlignmentFlag.AlignHCenter),
                  "Justify": AlignmentStyleWrapper(Qt.AlignmentFlag.AlignJustify),}
    # TODO more values

alignmentModel = AdaptedAlignmentModel()