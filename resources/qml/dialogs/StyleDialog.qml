import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import "../styleControls" as StyleControls


Dialog {
	id: dialog
	property var dialogDelegate
	 
	// Usually hidden unless call open()
	// visible: true
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
		// ??? This causes buttons to obscure content
		//anchors.fill: parent
		anchors.margins: 10

		StyleControls.ResettableSpinBox {
			id: bar
			text: "Any:Pen:Width"
			model: DocAnyAnyPenWidth
		}
		StyleControls.ResettableSpinBox {
			id: baz
			text: "Color"
			model: DocAnyAnyPenColor
		}
		StyleControls.ResettableSpinBox {
			id: docAnyAnyPenStyle
			text: "Style"
			model: DocAnyAnyPenStyle
		}
	}
	// a contentItem will not have buttons
}