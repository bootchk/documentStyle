// QML for stylesheet editor

import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import QmlDelegate 1.0

Item {
	DialogDelegate {
		id: dialogDelegate
		objectName: "dialogDelegate"
	}

	Dialog {
		id: styleDialog
	    visible: true
	    title: "Style dialog"
	    standardButtons: StandardButton.Ok | StandardButton.Cancel
	
	    contentItem: Rectangle {
	        color: "lightskyblue"
	        implicitWidth: 400
	        implicitHeight: 100
	        Text {
	            text: "Hello blue sky!"
	            color: "navy"
	            anchors.centerIn: parent
	        }
	    }
	}
	
	Connections {
	    target: dialogDelegate
	    onActivated: {
	    	console.log("Dialog activated")
	    	styleDialog.open()
	    }	
	 }
}