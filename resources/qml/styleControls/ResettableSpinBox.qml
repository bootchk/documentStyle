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
	id: row
	//anchors.fill: parent
	
	// Passed at instantiation
	property string text // label.text bound here
	property var model
	
	Label {
		id: label
		text: parent.text
	}
	// Demonstrate model owned by control.
	// Simpler than putting model outside control (which requires using Connection.)
	SpinBox {
		id: spinbox
		// bind to model.  It must be a NOTIFYable property!!!
		// value: model.value	
		
		// Model is a property
		// property QtObject model: Person{}
		
		// Usual signal on SpinBox.value property changed.
		onValueChanged: {
			print("SpinBox.value changed")
			// Access model exposed to here via context
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
		enabled: false
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
