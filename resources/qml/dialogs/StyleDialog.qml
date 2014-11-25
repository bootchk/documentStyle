import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

//import People 1.0
import "../styleControls" as StyleControls

Dialog {
	id: dialog
	 
	// Usually hidden unless call open()
	visible: true
	// Not a property: anchors.centerIn: parent
	// Not a property: flags: Qt.Dialog
	title: "My dialog"
	standardButtons: StandardButton.Ok | StandardButton.Cancel
	 
	onAccepted: {
		console.log("Accepted")
		dialogDelegate.accept()
	}
	 
	onRejected: {
		console.log("Rejected")
		dialogDelegate.reject()
	}
	
	Column {
		anchors.fill: parent
		anchors.margins: 10

		StyleControls.ResettableSpinBox {
			id: bar
			//row.label.text: "Width"	// override template
		}
		StyleControls.ResettableSpinBox {
			id: baz
			//row.label.text: "Color"
		}
	}
	// a contentItem will not have buttons
}