'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import Slot  # , QSize
from PySide.QtGui import QPushButton

class BuddyButton(QPushButton):
  '''
  A toggle button which resets a buddy Widget
  '''
  
  def __init__(self, name, initialState=False, buddyReset=None):
    '''
    '''
    super(BuddyButton, self).__init__(name)
    self.setEnabled(initialState)
    self.clicked.connect(self.handleClicked)
    self.buddyReset = buddyReset  # buddy's reset method
    
    ## TODO Want it a constant size, but chosen by the framework.
    ## setFixedSize() is not platform independent
    ## self.setFixedSize(60, 25)
    
  # QPushButton.toggle() is for "checked", but this button is not checkable
  @Slot()
  def handleClicked(self):
    '''
    Toggle behaviour: clicking disables.
    Action: reset buddy
    '''
    assert self.isEnabled()
    self.setEnabled(False)
    # print "calling buddyReset", self.buddyReset
    self.buddyReset()

  """
  def sizeHint(self):
    return QSize(40,28)
  """