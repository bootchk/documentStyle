// QML for stylesheet editor
// The shell with delegate and connections.

import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import QmlDelegate 1.0
import "dialogs" as MyDialogs

Item {
	DialogDelegate {
		id: userDialogDelegate
		objectName: "userDialogDelegate"
	}

	MyDialogs.StyleDialog {
		id: styleDialog
		title: "User Style Sheet"
		dialogDelegate: userDialogDelegate
	}
	
	Connections {
	    target: userDialogDelegate
	    onActivated: {
	    	console.log("Dialog activated")
	    	styleDialog.open()
	    	console.log("After dialog activated")
	    	console.assert(styleDialog.visible)
	    }	
	 }
	 Connections {
    	target: styleDialog
    	onVisibleChanged: console.log("Dialog visible changed")
	}
}