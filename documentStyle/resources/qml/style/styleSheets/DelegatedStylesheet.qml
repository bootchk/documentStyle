/*
QML for stylesheet editor.

This is outer shell with delegate and connections.
*/

import QtQuick 2.4

import QmlDelegate 1.0
import "../dialogs" as MyDialogs

Item {
	id: stylesheetWindow
	
	// specialized at instantiation
	property var dialogContentsURL
	property string titlePrefix
	
	// Delegate allowing Python side to open this dialog
	DialogDelegate {
		id: dialogDelegate
		objectName: "dialogDelegate"
	}
	
	// Subdialogs e.g. StyleColorDialog are owned by controls that use them
	
	MyDialogs.StyleDialog {
		id: styleDialog
		title: titlePrefix + " Style"
		dialogDelegate: dialogDelegate
		dialogSourceURL: dialogContentsURL
		
		Component.onCompleted: {
			print(x, y, width, height)
			console.assert(typeof stylesheetModel != 'undefined', "stylesheetModel is undefined")
		}
	}
	
	Connections {
	    target: dialogDelegate
	    onActivated: {
	    	console.log("Dialog activated from PyQt business side")
	    	stylesheetWindow.x = 400	// TEMP test
	    	stylesheetWindow.y = 400
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