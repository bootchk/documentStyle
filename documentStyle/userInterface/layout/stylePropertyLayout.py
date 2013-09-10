'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt4.QtGui import QHBoxLayout, QLabel # QPushButton, QSlider, QColor, QFont, QBoxLayout, 

from ..resettableControls.doubleSpinBox import ResettableDoubleSpinBox
from ..resettableControls.spinBox import ResettableSpinBox

from ..resettableControls.stylePickerWidget.colorPickerWidget import ColorPicker
from ..resettableControls.stylePickerWidget.fontPickerWidget import FontPicker
from ..resettableControls.comboBox import StyleComboBox
from ..resettableControls.buddyButton import BuddyIconButton

from documentStyle.debugDecorator import reportReturn

'''
Coupling:
Buddy knows BuddiedControl and vice versa, and call certain methods on each other.
Buddy also emits userReset signal handled by BuddiedControl.
BuddiedControl does not emit any signals to Buddy (only setEnabled() it.)

Call chain:
user changes BuddiedControl Widget
BuddiedControl Widget issues signal valueChanged
StylePropertyLayout.onValueChanged handles it:
- copies widget value to StyleProperty (state becomes not isReset())
- calls BuddyButton.setEnabled(True) (since user touched.)

Call chain:
user clicks BuddyButton (to reset)
BuddyButton calls Resettable.doUserReset()
doUserReset:
- resets StyleProperty (model)
- copies model to BuddiedControl Widget
-- Widget emits valueChanged
-- onValueChanged copies from widget back to model, which unresets it
-- onValueChanged calls BuddyButton.setEnabled(True)
- !!! again resets StyleProperty
BuddyButton emits userReset
StylePropertyLayout.onUserReset handles it:
- calls buddyButton.setEnabled(False) (not resettable until touched again.)

'''

class StylePropertyLayout(QHBoxLayout):
  '''
  Layout for a StyleProperty.  
  IOW a cooperating set of widgets that act as one.
  A better name is: LabeledResettableControlWidget
  
  Layout includes:
  - name: label
  - value: controlWidget that gets/sets parent StyleProperty on valueChange
  - buddyButton that undoes changes (reverts to original, inherited value)
  
  Thus a user's value change MAY propagate in real time, not wait for dialog accept.
  Whether it does so depends on whether StyleProperty propagates?
  
  Note we use the word 'reset'.
  But that does not mean to a 'default'.
  It means revert to some 'valueToResetTo', 
  which may be a value which was derived through previous cascade.
  '''


  def __init__(self, parentStyleProperty):
    '''
    
    '''
    super(StylePropertyLayout, self).__init__()
    
    # self.setDirection(QBoxLayout.RightToLeft)
    
    self.model = parentStyleProperty
    
    self._layoutChildWidgets(self.model)
    
    self.controlWidget.setValue(self.model.get()) # initial value
    
    '''
    Note possible race over BuddyButton.setEnabled.
    It is NOT a race if signals are immediate (not queued) and because of the way code is structured:
    when BuddyButton is clicked, it calls Resettable.doUserReset, which changes controlWidget to the reset value 
    (which emits valueChanged, which sets value of property AND sets isReset=False AND setEnabled(True) 
    and then emits userReset (which setEnabled(False) the BuddyButton).
    '''
    # connect valueChanged to self handler, not connect directly to buddyButton
    result = self.controlWidget.valueChanged.connect(self.onValueChanged)
    # PySide assert result
    result = self.buddyButton.userReset.connect(self.onUserReset)
    # PySide assert result
    
    
    
  def _layoutChildWidgets(self, model):
    '''
    Create and layout child widgets.
    
    Note layout strategy: 
    Children added left to right.
    Middle widget has non-zero stretch and expands.
    The resulting layout of a column of these layouts has:
    - a fixed width column of buddy buttons, right aligned.
    - control values and their control arrows right aligned to the buddy buttons.
    
    TODO maybe the controls should be left aligned to the labels?
    '''
    # Child: label
    self.addWidget(QLabel(self.model.name))
    
    # Child: Control
    # Some widgets don't use model
    self.controlWidget = self.createControlWidget(model) # delegate to subclass
    self.addWidget(self.controlWidget, stretch=1)  # TODO, stretch=0, alignment=Qt.AlignLeft)
   
    # Child: Buddy button
    self.buddyButton = BuddyIconButton("Inherit", 
                                initialState = not model.isReset(),
                                buddiedControl = self.controlWidget)
    self.addWidget(self.buddyButton)
   
   
   
    '''
    Each model must implement:
    @Slot(<type>)
    def set(self, value):
      assert isinstance(value, <type>)
      ...
      assert self.get() == value
    '''
    
  @reportReturn
  def onUserReset(self):
    '''
    On signal userReset, meaning buddy was pushed and already set my value.
    This is a circular signal problem:
    when buddyButton resets value, signal valueChanged enables buddyButton to wrong state.
    '''
    self.buddyButton.setEnabled(False)
    
  
  # Can't use @report here, called with varying args?
  def onValueChanged(self):
    '''
    On signal valueChanged:
    - transfer value from view to model.
    - set enable state of buddyButton
    Agnostic of type.
    '''
    self.propagateValueFromWidgetToModel()
    '''
    !!! valueChanged is emitted even when anyone (buddyButton) is programatically
    changing value to valueToResetTo.
    Any other valueChange means reset (buddyButton) should be enabled.
    So we setEnabled(True) it here, and if buddyButton is resetting self,
    buddyButton also emits userReset signal, which onUserReset() then setEnabled(False).
    '''
    self.buddyButton.setEnabled(True)
    
    
  def propagateValueFromWidgetToModel(self):
    changedValue = self.controlWidget.value()
    self.model.setPropertyValue(changedValue)
    
    
  def createControlWidget(self, model):
    raise NotImplementedError # deferred
  
  



class NumericStylePropertyLayout(StylePropertyLayout):
  
  def initializeWidgetRanges(self, widget, model):
    assert model.maximum >= model.minimum
    widget.setRange(model.minimum, model.maximum)
    widget.setSingleStep(model.singleStep)
    widget.setValue(model.minimum)
    #print "Widget max", widget.maximum()
    assert widget.hasAcceptableInput()
  
  
    
class FloatStylePropertyLayout(NumericStylePropertyLayout):
  
  def createControlWidget(self, model):
    widget = ResettableDoubleSpinBox(resettableValue = model.resettableValue)
    ## widget.setRange(model.minimum, model.maximum)
    self.initializeWidgetRanges(widget, model)
    return widget



class IntStylePropertyLayout(NumericStylePropertyLayout):
    
  def createControlWidget(self, model):
    widget = ResettableSpinBox(resettableValue = model.resettableValue)
    self.initializeWidgetRanges(widget, model)
    # TODO units suffix ?
    return widget



class ComboBoxStylePropertyLayout(StylePropertyLayout):
    
  def createControlWidget(self, model):
    widget = StyleComboBox(model=model.model, 
                           resettableValue = model.resettableValue)
    return widget
  
    
class ColorStylePropertyLayout(StylePropertyLayout):
  
  def createControlWidget(self, model):
    return ColorPicker(resettableValue = model.resettableValue)

    
    
class FontStylePropertyLayout(StylePropertyLayout):
  
  def createControlWidget(self, model):
    return FontPicker(resettableValue = model.resettableValue)
    
  