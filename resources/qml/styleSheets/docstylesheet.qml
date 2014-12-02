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
		model: stylesheetModel.selectResettableValueByStringSelector("*.*.Pen.Color")
	}

	MyDialogs.StyleDialog {
		id: styleDialog
		title: "Doc Style Sheet"
		dialogDelegate: docDialogDelegate
		// Get model from context
		// Global:  property var formationModel: stylesheetModel
		
		/*
		onVisibleChanged: {
			console.log("Dialog visible changed")
			console.log(styleDialog.visible)
		}
		*/
		Component.onCompleted: {
			print(x, y, width, height)
			console.assert(typeof stylesheetModel != 'undefined', "stylesheetModel is undefined")
		}
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