'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
import copy

from PySide.QtGui import QDialog, QFont

from styleSheet import StyleSheet

from documentStyle.styling.stylingAct import StylingAct
from documentStyle.styling.stylingActSet import StylingActSet
from documentStyle.styling.stylingActSetCollection import StylingActSetCollection

from documentStyle.selector import newAllSelector
# from userInterface.noneditableStyleDialog import NoneditableStyleDialog
from documentStyle.userInterface.styleDialog.styleDialog import StyleSheetDialog

from documentStyle.debugDecorator import report


class IntermediateStyleSheet(StyleSheet):
  '''
  A StyleSheet that is intermediate between DocumentElementStyleSheet and AppStyleSheet.
  
  Usual subclasses are UserStyleSheet and DocStyleSheet.
  See class hierarchy in super's documentation.
  
  Specializes StyleSheet:
  - cascades
  - editable
  '''
  def __init__(self, parent, name):
    StyleSheet.__init__(self, parent, name)
    # Collection may include many NamedStylingActSets
    self.stylingActSetCollection = StylingActSetCollection()
    
  
  def _dump(self):
    print "Displaying intermediate style sheet's stylingActSetCollection"  # name from formation?
    print self.stylingActSetCollection
    
  @report
  def getFormation(self, selector):
    '''
    Crux of cascading:
    - resolve name indirection on selector
    - ask parent for format
    - apply my inline styling to format
    
    Part of recursive walk through Formations.
    Pre- and post- recursion processing occurs.
    '''
    ''' Pre-recursion processing. '''
    '''
    TODO indirect name resolution
    Pre-visit, if the selector selects a named StylingActSet that 
    in turn refers to another named StylingActSet, the selector must be expanded
    to include the referred to name.
    '''
    
    ''' Recurse: cascade: get Formation from parent. '''
    formation = self.parent.getFormation(selector)
    
    ''' Post-recursion processing. '''
    #print "Uncascaded stylesheet", selector, repr(formation)
    # StyleProperties show whether overridden from previous cascade.  Reset all to "inherited"
    formation.resetResettableStyleProperties()
    self._overrideFormationBySelectedStylingActs(formation, selector)
    #print "Cascaded stylesheet", repr(formation)

    return formation


  def _overrideFormationBySelectedStylingActs(self, formation, selector):
    '''
    Apply my StylingActSets to formation, selected by selector.
    
    Selector delimits formation.  Select StylingActSets that apply to delimited formation.
    '''
    for stylingActSet in self.stylingActSetCollection.generateMatchingStylingActSets(selector):
      stylingActSet.applyToFormation(formation)
      
  
  def edit(self):
    '''
    Let user edit style sheet.  I.E.:
    - modify a SAS
    - delete a SAS
    - or append SAS
    '''
    # testing: canned SAS
    # self.testSAS()
  
    editedFormation = self.getFormation(newAllSelector())
    assert editedFormation is not None
    # dialog = NoneditableStyleDialog(parentWindow=None, formation=formation)
    
    # parentWindow is document so dialog centers in document.  If parentWindow were mainWindow (toplevel), Qt not center dialog
    dialog = StyleSheetDialog(formation=editedFormation)
    dialog.exec_()
    if dialog.result() == QDialog.Accepted:
      self.reflectEditsToStylingActSetCollection(editedFormation)
    
    # Since this is intermediate (user or doc) stylesheet, restyle all DocumentElements
    self.styleSheetChanged.emit()
    

  def reflectEditsToStylingActSetCollection(self, editedFormation):
    '''
    Iterate over top level formations of editedFormation
    (each top level is a group of edits to be a SAS.)
    each that has been changed should reflect itself to one of my StylingActSets
    '''
    for topLevelFormation in editedFormation:
      '''
      TODO optimization: only if subformation edited.
      Otherwise, SASCollection has many empty SAS?
      '''
      # when formation was derived through None stylingActSet, create a new one.
      target = self.stylingActSetCollection.getOrNew(topLevelFormation.selector())
      editedFormation.reflectToStylingActSet(derivingStylingActSet=target)
    
  
  def getSerializable(self):
    '''
    Instance that is minimally essential to represent state: StylingActs.
    
    Implementation notes:
    1.  deepcopy so subsequent changes to my copy does not change returned copy
    '''
    return copy.deepcopy(self.stylingActSetCollection)

  def resetFromSerializable(self, serializable):
    '''
    Restore to prior state.  
    
    Implementation notes:
    1.  deepcopy so subsequent changes to my copy does not change passed copy
    2.  Requires recomputation (cascading) which signal styleSheetChanged will trigger.
    '''
    self.stylingActSetCollection = copy.deepcopy(serializable)
    self.styleSheetChanged.emit() # force cascade and restyling of all styled instances
  
  

  def testSAS(self):
    # Canned SAS's for testing
    stylingActSet = StylingActSet()
    
    from selector import Selector

    # These SAS must be well-formed: not specify a instrument, field that doesn't apply to the DEType
    """
    For Shape morph:
    
    selector = Selector(name="*", DEType="Shape", instrument="Brush", field="Color")
    stylingAct = StylingAct(selector, color) # Qt.red) # or "red" ?
    stylingActSet.append(stylingAct)
    
    # Must also set Style: defaults to NoBrush
    selector = Selector(name="*", DEType="Shape", instrument="Brush", field="Style")
    stylingAct = StylingAct(selector, Qt.SolidPattern)
    stylingActSet.append(stylingAct)
    """
    
    # For Text morph
    selector = Selector(name="*", DEType="Text", instrument="Character", field="Font")
    stylingAct = StylingAct(selector, QFont("Times")) # "Helvetica")
    stylingActSet.put(stylingAct)
    """
    selector = Selector(name="*", DEType="Text", instrument="Character", field="FontWeight")
    stylingAct = StylingAct(selector, 75)  # QFont::Bold
    stylingActSet.append(stylingAct)
    
    selector = Selector(name="*", DEType="Text", instrument="Block", field="Alignment")
    stylingAct = StylingAct(selector, Qt.AlignRight)
    stylingActSet.append(stylingAct)
    
    selector = Selector(name="*", DEType="Text", instrument="Block", field="Indent")
    stylingAct = StylingAct(selector, 5)
    stylingActSet.append(stylingAct)
    
    # For Pixmap morph
    selector = Selector(name="*", DEType="Text", instrument="Opacity", field="Opacity")
    stylingAct = StylingAct(selector, 0.5)
    stylingActSet.append(stylingAct)
    """
    
    self.StylingActSetCollection.put(stylingActSet)
    

  


