'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtGui import QHBoxLayout, QBoxLayout, QLabel # QPushButton, QSlider, QColor, QFont

from ..resettableDoubleSpinBox import ResettableDoubleSpinBox
from ..resettableSpinBox import ResettableSpinBox

from ..stylePickerWidget.colorPickerWidget import ColorPicker
from ..stylePickerWidget.fontPickerWidget import FontPicker
from ..styleComboBox import StyleComboBox
from ..buddyButton import BuddyButton


'''
Chain of command:
user changes a style control Widget
Widget issues signal valueChanged
StyleProperty handles it and 

MAY issue signal ???
Formation may handle signal and issue signal ???
DocumentElement OR StyleSheet may handle signal and update self

OR 

StyleProperty does NOT issue signal
when Widget closed, Formation applied to DocumentElement
At that time, Formation gets value from StyleProperty
'''

class StylePropertyLayout(QHBoxLayout):
  '''
  Layout for a StyleProperty.
  
  Layout includes:
  - name
  - value: controlWidget that gets/sets parent StyleProperty on valueChange
  - buddyButton that undoes changes (reverts to original, inherited value)
  
  Thus a user's value change MAY propagate in real time, not wait for dialog accept.
  Whether it does so depends on whether StyleProperty propagates?
  '''


  def __init__(self, parentStyleProperty):
    '''
    
    '''
    super(StylePropertyLayout, self).__init__()
    
    # self.setDirection(QBoxLayout.RightToLeft)
    
    self.parentStyleProperty = parentStyleProperty
    self.addWidget(QLabel(parentStyleProperty.name))
    
    # Control widget
    # Some widgets don't use parentStyleProperty
    self.controlWidget = self.createControlWidget(self.parentStyleProperty)
    self.addWidget(self.controlWidget)  # TODO, stretch=0, alignment=Qt.AlignLeft)
    self.controlWidget.setValue(self.parentStyleProperty.get()) # initial value
    
    # only one connect to valueChanged, not connect directly to buddyButton
    result = self.controlWidget.valueChanged.connect(self.propagateValueFromWidgetToModel)
    assert result
    
    # Buddy button
    self.buddyButton = BuddyButton("Inherit", 
                                initialState= not parentStyleProperty.isReset(),
                                # Reset the view, not the model.  View will change the model.
                                buddyReset=self.controlWidget.reset)  # pass reset method
    self.addWidget(self.buddyButton)
    
   
    '''
    Each parentStyleProperty must implement:
    @Slot(<type>)
    def set(self, value):
      assert isinstance(value, <type>)
      ...
      assert self.get() == value
    '''
  
  
  def propagateValueFromWidgetToModel(self):
    '''
    On signal valueChanged:
    - transfer value from view to model.
    - set enable state of buddyButton
    Agnostic of type.
    '''
    changedValue = self.controlWidget.value()
    #print "propagateValueFromWidgetToModel", changedValue
    self.parentStyleProperty.set(changedValue)
    if not self.parentStyleProperty.isReset():
      self.buddyButton.setEnabled(True)
    
    
  def createControlWidget(self, parentStyleProperty):
    raise NotImplementedError # deferred
  
  



  
    
class FloatStylePropertyLayout(StylePropertyLayout):
  
  def createControlWidget(self, parentStyleProperty):
    widget = ResettableDoubleSpinBox(resettableValue = parentStyleProperty.resettableValue)
    widget.setRange(parentStyleProperty.minimum, parentStyleProperty.maximum)
    return widget



class IntStylePropertyLayout(StylePropertyLayout):
    
  def createControlWidget(self, parentStyleProperty):
    widget = ResettableSpinBox(resettableValue = parentStyleProperty.resettableValue)
    assert parentStyleProperty.maximum > parentStyleProperty.minimum
    widget.setRange(parentStyleProperty.minimum, parentStyleProperty.maximum)
    widget.setValue(parentStyleProperty.minimum)
    assert widget.hasAcceptableInput()
    # TODO units suffix
    return widget



class ComboBoxStylePropertyLayout(StylePropertyLayout):
    
  def createControlWidget(self, parentStyleProperty):
    widget = StyleComboBox(model=parentStyleProperty.model, 
                           resettableValue = parentStyleProperty.resettableValue)
    return widget
  
    
class ColorStylePropertyLayout(StylePropertyLayout):
  
  def createControlWidget(self, parentStyleProperty):
    return ColorPicker(resettableValue = parentStyleProperty.resettableValue)

    
    
class FontStylePropertyLayout(StylePropertyLayout):
  
  def createControlWidget(self, parentStyleProperty):
    return FontPicker(resettableValue = parentStyleProperty.resettableValue)
    
  