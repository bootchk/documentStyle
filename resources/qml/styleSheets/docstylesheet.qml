/*
QML for stylesheet editor.

This is outer shell with delegate and connections.

Other notes:
1. stylesheetModel is in root context and is globally referenced
2. other dialogs are owned by components (e.g. style dialog owned by font style control)
3. Whether the 'dialog' is modal, or has  buttons, can be changed later
*/


import QtQuick 2.3

import QmlDelegate 1.0
import "../dialogs" as MyDialogs

Item {
	// Delegate allowing Python side to open this dialog
	DialogDelegate {
		id: docDialogDelegate
		objectName: "docDialogDelegate"
	}
	
	// TODO This is specialized for Pen, need others for Brush, etc.
	MyDialogs.StyleColorDialog {
		id: colorDialog
		model: stylesheetModel.selectResettableValueByStringSelector("*.*.Pen.Color")
	}
	
	MyDialogs.StyleDialog {
		id: styleDialog
		title: "Doc Style Sheet"
		dialogDelegate: docDialogDelegate
		
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