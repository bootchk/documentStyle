import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import People 1.0

/*
 
See:
	-userInterface.resettableControls.spinBox.py
	-userInterface.layout.stylePropertyLayout.py
which are the QWidget version of this QML.

Row:  [label, control, reset button]

The reset button resets the control.
*/ 

Row {
	//anchors.fill: parent
	
	// Passed at instantiation
	property string text // label.text bound here
	// This component is generalized with a passed model and selector
	property var model
	property string selector: ""
	
	Label {
		text: parent.text
	}
	// Demonstrate model owned by control.
	// Simpler than putting model outside control (which requires using Connection.)
	SpinBox {
		id: spinbox	// referenced by reset button
		// Don't bind to model, because we control it only?  It must be a NOTIFYable property!!!
		// OR bind to value so that on second opening, it follows the model
		value: model.value	
		
		// Model is a property
		// property QtObject model: Person{}
		
		// Usual signal on SpinBox.value property changed.
		onValueChanged: {
			print("SpinBox.value changed")
			// Access model from context passed into this component
			model.value = value	// view=>model
			// model touched is NOT a side effect of setting value    
			model.touched = true
			resetButton.enabled = true
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
	Button {
		/*
		Model is resettable.
		We do not need to update view from model now,
		spinBox.value is bound to the model.
		*/
		id: resetButton
		text: "Reset"
		// Bind to model
		enabled: ! model.isReset
		onClicked: {
			print("button clicked")
			// Reset model
			model.isReset = true
			model.touched = true
			spinbox.value = model.value	// Do this ourselves, instead of from signal from model
			// Assert view value is reset also
			print("model.value", model.value)
			// Button state
			enabled = false
		}
	}
}
