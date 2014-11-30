// QML for stylesheet editor
// The shell with delegate and connections.

import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2
//import QtQuick.Window 2.0

import QmlDelegate 1.0
import "../dialogs" as MyDialogs

Item {
	DialogDelegate {
		id: docDialogDelegate
		objectName: "docDialogDelegate"
	}
	
	MyDialogs.StyleColorDialog {
		id: colorDialog
		model: DocAnyAnyPenColor
	}

	MyDialogs.StyleDialog {
		id: styleDialog
		title: "Doc Style Sheet"
		dialogDelegate: docDialogDelegate
		
		/*
		onVisibleChanged: {
			console.log("Dialog visible changed")
			console.log(styleDialog.visible)
		}
		*/
	}
	
	Connections {
	    target: docDialogDelegate
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