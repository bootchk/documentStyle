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
		model: parent.domain	// TODO parent. not needed
		// TODO alias for resetButton??  Seems to work without it
		currentIndex: parent.model.value
		         
		onActivated: {
			/*
			 * Similar to currentIndexChanged, but only with user input.
			 * onCurrentIndexChanged comes on initialization without user input.
			 * Also, this has a formal parameter "index" which is not same as currentIndex
			 */
			console.debug("CombBox.onActivated", index)
			// Note index is actual parameter of signal, not same as currentIndex
			// OLD, for continguous enums: parent.model.value = index
			// New use a list of [text,value] pairs i.e. ListModel of ListElements
			parent.model.value = model.get(index).value	
			parent.model.touched = true
		}
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: combobox
	}
}