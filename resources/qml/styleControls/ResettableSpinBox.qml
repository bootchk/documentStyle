import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import People 1.0

// Row:  [label, control, reset button]

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
		
		// Model is a property
		// property QtObject model: Person{}
		
		// Usual signal on SpinBox.value property changed.
		onValueChanged: {
			print("SpinBox.value changed")
			// Access model exposed to here in context
			model.value = value		// view->model
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
		id: resetButton
		text: "Reset"
		enabled: false
		onClicked: {
			print("button clicked")
			// Reset model
			model.reset = true
			model.touched = true
			// TODO broken: model.value doesn't change
			// Reset view also
			spinbox.value = model.value
			// Button state
			enabled = false
		}
	}
}
