import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import People 1.0

Dialog {
     id: dialog
     
     // Usually hidden unless call open()
     // visible: true
     // Not a property: anchors.centerIn: parent
     // Not a property: flags: Qt.Dialog
     title: "My dialog"
	 standardButtons: StandardButton.Ok | StandardButton.Cancel
	 
	 //Calendar {
	 //	id: calendar
	//	onDoubleClicked: dateDialog.click(StandardButton.Save)
	//	}
	
	Column {
		anchors.fill: parent
		anchors.margins: 10

		Row {
			Label {
				id: label
				text: "foo"
			}
			// Demonstrate model owned by control.
			// Simpler than putting model outside control (which requires using Connection.)
			SpinBox {
				id: spinbox
				
				// Model is a property
				property QtObject model: Person{}
				
				// Usual signal on SpinBox.value property changed.
				onValueChanged: print("SpinBox.value changed")
				
				// special signal on SpinBox lose focus
				onEditingFinished: {
					print("SpinBox.editingFinished")
					model.activate()	// Relay to business logic
				}
				
				// This executed if business logic changes model value.
				// The view should change to reflect new value
				onModelChanged: print("Model changed by business logic")
			}
			Button {
				id: button
				text: "Reset"
				onClicked: print("button clicked")
			}
			
		}
	}
	// a contentItem will not have buttons
}