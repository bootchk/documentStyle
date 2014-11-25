import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import People 1.0

// Row:  [label, control, reset button]

Row {
	id: row
	
	Label {
		id: label
		text: "foo"
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
			DocAnyAnyPenWidth.value = 10
			DocAnyAnyPenWidth.touched = true
			}
		
		// special signal on SpinBox lose focus
		onEditingFinished: {
			print("SpinBox.editingFinished")
			// model.activate()	// Relay to business logic
		}
		
		// This executed if business logic changes model value.
		// The view should change to reflect new value
		// onModelChanged: print("Model changed by business logic")
	}
	Button {
		id: button
		text: "Reset"
		onClicked: {
			print("button clicked")
			DocAnyAnyPenWidth.reset = true	// side effect on model, but not on view???
			// TODO need to reset view also
			DocAnyAnyPenWidth.touched = true
		}
	}
}
