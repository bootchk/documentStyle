import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import "../styleControls" as MyControls

/*
 
See:
	-userInterface.resettableControls.spinBox.py
	-userInterface.layout.stylePropertyLayout.py
which are the QWidget version of this QML.

Row:  [label, control, reset button]

The reset button resets the control to an inherited value.
*/ 

Row {
	//anchors.fill: parent
	
	// Component is generalized, specialized with a passed [text, model, selector] at instantiation
	property string text // label.text bound here
	property var model
	property string selector
	
	// Optional specialization
	property alias controlDecimals: spinbox.decimals
	property alias controlStepSize: spinbox.stepSize
	property alias controlMinimumValue: spinbox.minimumValue
	property alias controlMaximumValue: spinbox.maximumValue
	
	Label {
		text: parent.text
	}
	// Demonstrate model owned by control.
	// Simpler than putting model outside control (which requires using Connection.)
	SpinBox {
		id: spinbox	// referenced by reset button
		
		/* 
		model.value must be a NOTIFYable property!!!
		Bind view value to model value so that on second opening, and on reset, it follows the model.
		Although the user is in charge, user can also change the model via the reset button.
		*/
		value: model.value	// model=>view
		
		/*
		Usual signal on view SpinBox.value property changed.
		This is NOT the signal valueChanged from model.
		*/
		onValueChanged: {
			print("SpinBox.value changed")
			// Access model from context passed into this component
			model.value = value	// view=>model
			// model touched is NOT a side effect of setting value    
			model.touched = true
			// Side effect of setting value 
			// resetButton.enabled = true
			}
		
		// special signal on SpinBox lose focus
		onEditingFinished: {
			print("SpinBox.editingFinished")
			// model.activate()	// Live Relay to business logic
			// For now, has batch dialog semantics
		}
		
		// This executed if business logic changes model value.
		// The view should change to reflect new value
		// onModelChanged: print("Model changed by business logic")
	}
	
	MyControls.ResetButton {
		model: parent.model
		buddyControl: spinbox
	}
}
