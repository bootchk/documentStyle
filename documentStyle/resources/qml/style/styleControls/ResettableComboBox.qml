import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.2

import "../styleControls" as MyControls

/*
 See: ResettableSpinBox which is the commented template for this.
 This is the equivalent of a QWidget.
*/ 
Row {
	spacing: 10
	
	property string text
	property var model
	property string selector
	property var domain	// combobox's sub model
	
	Label {
		id: label
		text: parent.text
	}
	
	ComboBox{
		id: combobox
		model: domain
		// TODO alias for resetButton??  Seems to work without it
		
		// TODO since model is a ListModel, convert from parent.model.value to ListModel.index to currentIndex
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
	
	Connections{
		target: model
		onValueChanged: {
			console.log("parent model value changed")
			//combobox.find()
		}	
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: combobox
	}
}
