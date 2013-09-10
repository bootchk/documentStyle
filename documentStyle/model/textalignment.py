'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt4.QtCore import Qt

from documentStyle.styleWrapper.styleWrapper import AlignmentStyleWrapper


class AdaptedAlignmentModel(object):
  '''
  Mimics a PyQt4 enum: has "values" attribute that is a dictionary
  
  Here, we limit to one dimension (horizontal) of two dimensional alignment
  '''
  def __init__(self):
    qtEnum = Qt # PySide qtEnum = Qt.AlignmentFlag
    self.values = {"Left": AlignmentStyleWrapper(qtEnum.AlignLeft),
                   "Right": AlignmentStyleWrapper(qtEnum.AlignRight),
                  "Center": AlignmentStyleWrapper(qtEnum.AlignHCenter),
                  "Justify": AlignmentStyleWrapper(qtEnum.AlignJustify),}
    # TODO more values

alignmentModel = AdaptedAlignmentModel()