'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal as Signal

from documentStyle.debugDecorator import report

class StyleSheet(QObject):  # QObject for signals
  '''
  A set of StylingActSet's that helps define appearance of DocumentElements.
  
  The usual class structure is (and distinguishing behavior):
  - StyleSheet
  --  AppStyleSheet: not editable, has defaults from the framework
  --  IntermediateStyleSheet: editable, has StylingActSetCollection
  ---   DocumentStyleSheet: persists with a Document
  ---   UserStyleSheet: persists with a user's preferences
  --  DocumentElementStyleSheet: editable but cannot have NamedStylingActSets.  Persists with a DocumentElement.
  
  Responsibilites:
  - support tree structuring of StyleSheets (cascading)
  - know StylingActs on self (subclass Intermediate)
  - get a Formation for a Selector
  - display self (some subclasses editable i.e. non-empty stylingActSet)
  - signal when changed (editable subclasses)
  
  It is NOT a responsibility to persist.
  The AppStyleSheet subclass does NOT persist.  
  Subclasses IntermediateStyleSheet and DocumentElementStyleSheet DO persist.
  
  It is NOT a responsibility of StyleSheet to emit signal when cascade structure changes,
  i.e. when a StyleSheet in cascade is deserialized and inserted in the cascade.
  (But StyleSheetCascadion has that responsibility.)
  
  This is ABC, defining methods that should be reimplemented.
  '''

  styleSheetChanged = Signal()  # User accepted edit dialog
  styleSheetEditCanceled = Signal() # User canceled edit dialog

  def __init__(self, name=None):
    super(StyleSheet, self).__init__()
    self.parent = None
    self.name = name
  
  
  @report
  def setParent(self, parent):
    '''
    Parent is NOT set by init.
    One reason is that would interfere with pickling.
    See comment above: no signal, but polish needs to be done.
    '''
    assert isinstance(parent, StyleSheet)
    self.parent = parent
  
  
  def getFormation(self, selector):
    raise NotImplementedError, 'Deferred'

  
  def edit(self):
    raise NotImplementedError, 'Deferred'
  
