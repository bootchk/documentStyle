import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2

import "../styleControls" as MyControls

/*
 See: ResettableSpinBox which is the commented template for this.
 This is the equivalent of a QWidget.
*/ 
Row {
	property string text
	property var model
	property string selector
	property var domain	// combobox's sub model
	
	spacing: 10
	
	Label {
		id: label
		text: parent.text
	}
	
	ComboBox{
		id: combobox
		model: parent.domain	// 
		// TODO alias for resetButton??  Seems to work without it
		currentIndex: parent.model.value
		         
		onCurrentIndexChanged: {
			console.debug("currentIndexChanged")
			parent.model.value = currentIndex
			parent.model.touched = true
		}
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: combobox
	}
}
