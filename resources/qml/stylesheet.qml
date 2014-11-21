// QML for stylesheet editor
// The shell with delegate and connections.

import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2
//import QtQuick.Window 2.0

import QmlDelegate 1.0
import "dialogs" as MyDialogs

Item {
	DialogDelegate {
		id: dialogDelegate
		objectName: "dialogDelegate"
	}

	MyDialogs.Dialog2 {
		id: styleDialog
		
		onVisibleChanged: {
			console.log("Dialog visible changed")
			console.log(styleDialog.visible)
		}
	}
	
	Connections {
	    target: dialogDelegate
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