'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from .stylePropertyLayout import StylePropertyLayout

from ..resettableControls.doubleSpinBox import ResettableDoubleSpinBox
from ..resettableControls.spinBox import ResettableSpinBox

from ..resettableControls.stylePickerWidget.colorPickerWidget import ColorPicker
from ..resettableControls.stylePickerWidget.fontPickerWidget import FontPicker
from ..resettableControls.comboBox import StyleComboBox


'''
Subclasses of StylePropertyLayout specialized by type.
'''


class NumericStylePropertyLayout(StylePropertyLayout):
  '''
  Base class for Int and Float
  '''
  
  def initializeWidgetRanges(self, widget, domain):
    assert domain.maximum >= domain.minimum
    widget.setRange(domain.minimum, domain.maximum)
    widget.setSingleStep(domain.singleStep)
    widget.setValue(domain.minimum)
    #print "Widget max", widget.maximum()
    assert widget.hasAcceptableInput()
  
  
    
class FloatStylePropertyLayout(NumericStylePropertyLayout):
  
  def createControlWidget(self):
    widget = ResettableDoubleSpinBox(resettableValue = self.model)
    ## widget.setRange(domain.minimum, domain.maximum)
    self.initializeWidgetRanges(widget, self.domain)
    return widget



class IntStylePropertyLayout(NumericStylePropertyLayout):
    
  def createControlWidget(self):
    widget = ResettableSpinBox(resettableValue = self.model)
    self.initializeWidgetRanges(widget, self.domain)
    # TODO units suffix ?
    return widget



class ComboBoxStylePropertyLayout(StylePropertyLayout):
    
  def createControlWidget(self):
    widget = StyleComboBox(domainModel=self.domain.model,
                           resettableValue = self.model)
    return widget
  
    
class ColorStylePropertyLayout(StylePropertyLayout):
  
  def createControlWidget(self):
    # domain not used
    return ColorPicker(resettableValue = self.model)

    
    
class FontStylePropertyLayout(StylePropertyLayout):
  
  def createControlWidget(self):
    # domain not used
    return FontPicker(resettableValue = self.model)
    
  