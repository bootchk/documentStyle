'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

import documentStyle.config as config


class AdaptedAlignmentModel(object):
  '''
  Mimics a PyQt5 enum: has "values" attribute that is a dictionary
  
  Here, we limit to one dimension (horizontal) of two dimensional alignment
  '''
  def __init__(self):
    """
    OLD
    from PyQt5.QtCore import Qt
    qtEnum = Qt # PySide qtEnum = Qt.AlignmentFlag
    and values were AlignLeft AlignRight AlignHCenter AlignJustify
    NEW: values are continguous enum, adapted by our instrument wrapper
    """
    self.values = {config.i18ns.Left : 0, #qtEnum.AlignLeft,
                   config.i18ns.Right : 1, #qtEnum.AlignRight,
                  config.i18ns.Center : 2, #qtEnum.AlignHCenter,
                  config.i18ns.Justify : 3,  #qtEnum.AlignJustify,
                  }
    # TODO more values

  # Other models def default() but apparently it is not used?
