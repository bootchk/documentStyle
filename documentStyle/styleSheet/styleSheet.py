'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import QObject, Signal


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
  - persist TODO
  - signal when changed (editable subclasses)
  '''

  styleSheetChanged = Signal()


  def __init__(self, parent=None, name=None):
    super(StyleSheet, self).__init__()
    self.parent = parent
    self.name = name
      
  
  def getFormation(self, selector):
    raise NotImplementedError # deferred

  
  def edit(self):
    raise NotImplementedError # deferred



