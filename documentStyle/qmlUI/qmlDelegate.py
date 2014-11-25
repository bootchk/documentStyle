
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
# pyqtProperty
 
 

class QmlDelegate(QObject):
  '''
  Delegate between QML and Python.
  Typically for a QML dialog.
  
  A type that will be registered with QML.  
  Must be a sub-class of QObject.
  '''
  
  activated = Signal()
  accepted = Signal()
  rejected = Signal()
  
  '''
  Note connections (for instances) can be made from QML or from Python?
  
  Method must be slot to be callable/invokeable from QML JS.
  '''

  
  def activate(self):
    '''
    Emit activated signal.
    Called from business side.
    Connected in QML to Dialog.open()
    '''
    print("activate called, emitting activated")
    self.activated.emit()
  
  
  @Slot()
  def accept(self):
    '''
    Called from QML side.
    Connected in business side to a handler of dialog results (in shared model.)
    '''
    self.accepted.emit()
  
  @Slot()
  def reject(self):
    '''
    Opposite cohort of accept.
    '''
    self.rejected.emit()
    