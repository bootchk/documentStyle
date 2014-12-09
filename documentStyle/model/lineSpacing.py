'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

import documentStyle.config as config

class AdaptedLineSpacingModel(object):
  '''
  Mimics a PyQt5 enum: has "values" attribute that is a dictionary
  
  Here, line spacing is always proportional type of line spacing,
  and the values are in percent.
  '''
  def __init__(self):
    self.values = {config.i18ns.Single : 0,   #100,
                  config.i18ns.Double : 1, #200,
                  config.i18ns.OnePointFive : 2, # 150,
                  }
    # TODO more values