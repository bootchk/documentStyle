'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

#from PySide.QtCore import Qt
# from documentStyle.styleWrapper.styleWrapper import LineSpacingStyleWrapper


class AdaptedLineSpacingModel(object):
  '''
  Mimics a PySide enum: has "values" attribute that is a dictionary
  
  Here, line spacing is always proportional type of line spacing,
  and the values are in percent.
  '''
  def __init__(self):
    self.values = {"Single": 100,
                   "1.5": 150,
                  "Double": 200,
                  }
    # TODO more values

lineSpacingModel = AdaptedLineSpacingModel()