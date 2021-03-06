'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

#from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .styleSheet import StyleSheet

from documentStyle.styling.stylingAct import StylingAct
from documentStyle.styling.stylingActSet import StylingActSet
from documentStyle.styling.stylingActSetCollection import StylingActSetCollection

from documentStyle.selector import newAllSelector
from documentStyle.ui.dialogFactory import dialogFactory

from documentStyle.debugDecorator import report, reportReturn


class IntermediateStyleSheet(StyleSheet):
  '''
  A StyleSheet that is intermediate between DocumentElementStyleSheet and AppStyleSheet.
  
  Usual subclasses are UserStyleSheet and DocStyleSheet.
  See class hierarchy in super's documentation.
  
  Specializes StyleSheet:
  - cascades
  - editable
  '''
  def __init__(self, name):
    StyleSheet.__init__(self, name)
    # Collection may include many NamedStylingActSets
    self.stylingActSetCollection = StylingActSetCollection()
    
    
  def __repr__(self):
    return "IntermediateStyleSheet:" + self.name
  
  
  def _dump(self):
    print("Displaying intermediate style sheet's stylingActSetCollection")  # name from formation?
    print(self.stylingActSetCollection)
    
  def clear(self):
    ''' Reset by erasing styling acts. '''
    self.stylingActSetCollection = StylingActSetCollection()
    
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
    assert self.parent is not None, 'Cascade broken at ' + self.name
    formation = self.parent.getFormation(selector)
    
    ''' Post-recursion processing. '''
    #print "Uncascaded stylesheet", selector, repr(formation)
    '''
    StyleProperties show whether stylingAct applies (overrides) previous cascade.  
    Initialize all to show "not overridden" i.e. inherited.
    '''
    formation.rollStyleProperties()
    '''
    Now apply Styling Acts (override), changing state of StyleProperties from "not overridden" to "overridden".
    '''
    self._applySelectedStylingActs(formation, selector)
    #print "Cascaded stylesheet", repr(formation)

    return formation

  @reportReturn
  def _applySelectedStylingActs(self, formation, selector):
    '''
    Apply my StylingActSets to formation, selected by selector.
    For debugging, return count.
    
    Selector delimits formation.  Select StylingActSets that apply to delimited formation.
    '''
    assert selector == formation.selector # i.e., parameter selector is really superfluous
    count = 0
    for stylingActSet in self.stylingActSetCollection.generateMatchingStylingActSets(selector):
      count += 1
      # DEBUG uncomment this to see cascade in action
      #print("applySelectedStylingActSet from ", str(self), "to ", str(formation))
      stylingActSet.applyToFormation(formation)
    return count
      

  def createGui(self, parentWindow):
    '''
    Gui comprises a formation (a structured model) and a dialog(sic) that controls it.
    The dialog is a View.  View displays the model and controls it.
    One way: user is the only one controlling the model (not any other business logic.)
    After editing formation, it is reflected (converted) to StylingActs.
    The edited formation (or at least the contents) is then discarded.
    
    Formerly, this was created on the fly then discarded, over and over.
    
    Note the gui may be QWidget based, or QML based.
    For QML, we create the gui early so that we can expose the model to it.
    '''
    self.editedFormation = self.getFormation(newAllSelector())  # Temporary: previous is garbage collected.
    assert self.editedFormation is not None
    
    # parentWindow is document so dialog centers in document.  
    # If parentWindow were mainWindow (toplevel), Qt not center dialog
    self.dialog = dialogFactory.produceEditableDialog(parentWindow = parentWindow,
                                      formation=self.editedFormation, 
                                      titleParts = (self.name, "Style Sheet"))
                                      # WAS flags=Qt.Sheet)
                                      # but that is not needed if open() which is window modal
    self.dialog.connectSignals(acceptSlot=self.acceptEdit, cancelSlot=self.cancelEdit)
  
  
  '''
  Note dialog is created anew, and its signals are connected to these relay methods.
  However, one test app required reconnect to styleSheetEditCanceled before each call to edit().
  Could not reproduce in a test harness, but be aware.
  '''
  def acceptEdit(self):
    ''' Slot for signal accepted of dialog. Relay to caller as signal styleSheetChanged. '''
    #print(self.editedFormation._longRepr())
    print("IntermediateStyleSheet.acceptEdit")
    self.reflectEditsToStylingActSetCollection(self.editedFormation)
    '''
    Self is intermediate (user or doc or documentElement) stylesheet instance.
    Signals are emitted from instances.
    Slot for user and doc stylesheets signal will probably polish all DocumentElements.
    Slot for DocumentElementStyleSheet signal may be in a DocumentElement instance,
    or the signal may be unhandled, i.e. DocumentElement being edited will polish itself.
    '''
    self.styleSheetChanged.emit()
    
  def cancelEdit(self):
    ''' Slot for signal canceled from dialog.  Relay, because pps may want so they can exit a mode of editing. '''
    self.styleSheetEditCanceled.emit()
    
  @report
  def reflectEditsToStylingActSetCollection(self, editedFormation):
    '''
    Iterate over top level formations of editedFormation
    (each top level is a group of edits to be a SAS.)
    each that has been changed should reflect itself to one of my StylingActSets
    '''
    #beforeStylingActCount = self.stylingActSetCollection.countStylingActs()
    
    deletedCount = 0
    for topLevelFormation in editedFormation.generateSubformations():
      '''
      Optimization: only if subformation edited.
      Otherwise, SASCollection has many empty SAS?
      '''
      if topLevelFormation.isTouched(): # WAS isEdited():
        # when formation was derived through None stylingActSet, create a new one.
        #print("toplevelFormation isTouched")
        targetSAS = self.stylingActSetCollection.getMatchingOrNewStylingActSet(topLevelFormation.selector)
        beforeCount = len(targetSAS)
        deletedCount += editedFormation.reflectToStylingActSet(derivingStylingActSet=targetSAS)
        #print("Count styling acts before and after:", beforeCount, len(targetSAS))
        '''
        This is hacking for a ensure clause:
        if the user touched formation,
        it should change the sas in a verifiable way.
        
        If user in-lined, the count should go up.
        If the user reset, the count should go down.
        But its complicated by the fact that there could be offsetting changes in the count.
        
        afterCount = len(targetSAS)
        print(beforeCount, afterCount)
        assert afterCount >= (beforeCount - deletedCount)
    
        # TODO assertion on change to count: after = before - deleted + added
        #afterStylingActCount = self.stylingActSetCollection.countStylingActs()
        #print('Reflection results on', str(self))
        #print('before, after, deleted', beforeStylingActCount, afterStylingActCount, deletedCount)
        '''
    
  '''
  Persistence (pickling)
  '''
  
  def __reduce__(self):
    '''
    Implement pickling protocol 2 using reduce.
    Needed since unadorned StyleSheet is not pickleable (can't pickle QObject since signals.)
    
    Return tuple: (class factory, args to class factory, state dictionary)
    
    !!! Note we disown from parent: only pickle this StyleSheet, not the chain of styleSheets.
    Because pickling the cascade would finally attempt to pickle the AppStyleSheet, 
    which by design should NOT be pickled.
    '''
    #print "pickling stylesheet"
    ##WAS return (IntermediateStyleSheet, (self.name, ), {'stylingActSetCollection': self.stylingActSetCollection})
    ''' Since this method is inherited by DocumentElementStyleSheet, don't hardcode the class as IntermediateStyleSheet. '''
    return (self.__class__, (self.name, ), {'stylingActSetCollection': self.stylingActSetCollection})

  
  """
  OLD
  def getSerializable(self):
    '''
    Instance that is minimally essential to represent state: StylingActs.
    
    Implementation notes:
    1.  deepcopy so subsequent changes to my copy does not change returned copy
    '''
    return copy.deepcopy(self.stylingActSetCollection)

  #@report
  def resetFromSerializable(self, serializable):
    '''
    Restore to prior state.  
    
    Implementation notes:
    1.  deepcopy so subsequent changes to my copy does not change passed copy
    2.  Requires recomputation (cascading) which signal styleSheetChanged will trigger.
    '''
    self.stylingActSetCollection = copy.deepcopy(serializable)
    self.styleSheetChanged.emit() # force cascade and restyling of all styled instances
  """
  

  def testSAS(self):
    # Canned SAS's for testing
    stylingActSet = StylingActSet()
    
    from documentStyle.selector import Selector

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
    

  


