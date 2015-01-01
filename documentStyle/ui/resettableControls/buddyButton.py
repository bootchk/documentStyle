'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QPushButton, QToolButton, QStyle # QIcon

# Not used?
class BuddyPushButton(QPushButton):
  '''
  Toggle button which resets a buddy Widget
  '''
  
  def __init__(self, name, initialState=False, buddiedControl=None):
    super(BuddyPushButton, self).__init__(name)
    self.setEnabled(initialState)
    self.clicked.connect(self.handleClicked)
    self.buddiedControl = buddiedControl  # buddy's reset method
    
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
    self.buddiedControl.reset()




class BuddyIconButton(QToolButton):
  '''
  ToolButton variant of BuddyButton
  
  Icon is 'Undo', same meaning as 'Inherit' i.e. undo override.
  '''
  userReset = Signal()
  
  def __init__(self, name, initialState=False, buddiedControl=None):
    super(BuddyIconButton, self).__init__()
    # name not used?
    self._initIcon()
    self.setEnabled(initialState)
    self.clicked.connect(self.handleClicked)
    self.buddiedControl = buddiedControl  # buddy's reset method
    
  def _initIcon(self):
    
    # Portable: get icon from app's style.  SP means standard pixmap
    # Alternative is ArrowUp or ArrowBack
    icon = QCoreApplication.instance().style().standardIcon(QStyle.SP_BrowserReload)
    if not icon.isNull():
      self.setIcon(icon)
    else:
      # !!! Fail (0n older platforms (Classic Ubuntu?).  Fallback is up arrow.
      self.setArrowType(Qt.UpArrow)
    
    ##Not portable
    ##icon = QIcon.fromTheme("edit-undo", QIcon(":/undo.png"))
    ## TODO on Mac and Windows, you will have to bundle a compliant theme in one of your themeSearchPaths() 
    ## and set the appropriate themeName().
    
    
  # QPushButton.toggle() is for "checked", but this button is not checkable
  @Slot()
  def handleClicked(self):
    '''
    Toggle behaviour: clicking disables.
    Action: reset buddy
    '''
    assert self.isEnabled()
    self.setEnabled(False)  # TODO not needed
    self.buddiedControl.doUserReset() # tell buddied to reset its value
    self.userReset.emit() # buddied will setEnabled me to proper state


  """
  def sizeHint(self):
    return QSize(40,28)
  """