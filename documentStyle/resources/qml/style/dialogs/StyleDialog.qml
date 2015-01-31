import QtQuick 2.3
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.1

import "../dialogContents" as MyDialogContents

// Main editor of stylesheet, current design: a dialog.
Dialog {
	id: dialog
	modality: Qt.ApplicationModal
	
	property var dialogDelegate
	property var dialogSourceURL
	 
	// Usually hidden unless call open()
	// visible: true
	// Not a property: anchors.centerIn: parent
	// Not a property: flags: Qt.Dialog
	title: "template"
	standardButtons: StandardButton.Ok | StandardButton.Cancel
	//minimumWidth: 400
	//Layout.fillWidth: true
	
	/*
	Contents is separate file, unrelated to buttons and handlers.
	
	Style dialog contents depends (varies with) model, i.e. is dynamic.
	E.g. Full style sheet is tabbed, style sheet for Tool is not tabbed, etc.
	*/ 
	Loader { source: dialogSourceURL }
	
	onAccepted: {
		console.log("Accepted")
		dialogDelegate.accept()
	}
	 
	onRejected: {
		console.log("Rejected")
		dialogDelegate.reject()
	}
	
	
}