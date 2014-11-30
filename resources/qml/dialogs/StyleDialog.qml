import QtQuick 2.3
//import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import "../dialogContents" as MyDialogContents


Dialog {
	id: dialog
	property var dialogDelegate
	 
	// Usually hidden unless call open()
	// visible: true
	// Not a property: anchors.centerIn: parent
	// Not a property: flags: Qt.Dialog
	title: "My dialog"
	standardButtons: StandardButton.Ok | StandardButton.Cancel
	//minimumWidth: 400
	//Layout.fillWidth: true
	 
	onAccepted: {
		console.log("Accepted")
		dialogDelegate.accept()
	}
	 
	onRejected: {
		console.log("Rejected")
		dialogDelegate.reject()
	}
	
	MyDialogContents.StyleDialogContents{}
}