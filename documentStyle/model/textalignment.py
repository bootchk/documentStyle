'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import Qt

import documentStyle.config as config
#from documentStyle.styleWrapper.styleWrapper import AlignmentStyleWrapper


class AdaptedAlignmentModel(object):
  '''
  Mimics a PyQt5 enum: has "values" attribute that is a dictionary
  
  Here, we limit to one dimension (horizontal) of two dimensional alignment
  '''
  def __init__(self):
    qtEnum = Qt # PySide qtEnum = Qt.AlignmentFlag
    """
    PySide
    self.values = {"Left": AlignmentStyleWrapper(qtEnum.AlignLeft),
                   "Right": AlignmentStyleWrapper(qtEnum.AlignRight),
                  "Center": AlignmentStyleWrapper(qtEnum.AlignHCenter),
                  "Justify": AlignmentStyleWrapper(qtEnum.AlignJustify),}
    """
    self.values = {config.i18ns.Left : qtEnum.AlignLeft,
                   config.i18ns.Right : qtEnum.AlignRight,
                  config.i18ns.Center : qtEnum.AlignHCenter,
                  config.i18ns.Justify : qtEnum.AlignJustify,}
    # TODO more values

  # Other models def default() but apparently it is not used?
