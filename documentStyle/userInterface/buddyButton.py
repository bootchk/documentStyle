'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import Qt, Slot
from PySide.QtCore import QCoreApplication
from PySide.QtGui import QPushButton, QToolButton, QStyle # QIcon

class BuddyPushButton(QPushButton):
  '''
  Toggle button which resets a buddy Widget
  '''
  
  def __init__(self, name, initialState=False, buddyReset=None):
    super(BuddyPushButton, self).__init__(name)
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
    self.buddyReset()




class BuddyIconButton(QToolButton):
  '''
  ToolButton variant of BuddyButton
  
  Icon is 'Undo', same meaning as 'Inherit' i.e. undo override.
  '''
  
  def __init__(self, name, initialState=False, buddyReset=None):
    super(BuddyIconButton, self).__init__()
    self._initIcon()
    self.setEnabled(initialState)
    self.clicked.connect(self.handleClicked)
    self.buddyReset = buddyReset  # buddy's reset method
    
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
    self.setEnabled(False)
    self.buddyReset()


  """
  def sizeHint(self):
    return QSize(40,28)
  """