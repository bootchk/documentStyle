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
			parent.model.value = index	// Note this is actual parameter of signal, not same as currentIndex
			parent.model.touched = true
		}
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: combobox
	}
}

/*
 * How to use a list model (non-contiguous enum)
 * 
 * ComboBox {
    currentIndex: 2
    model: ListModel {
        id: cbItems
        ListElement { text: "Banana"; color: "Yellow" }
        ListElement { text: "Apple"; color: "Green" }
        ListElement { text: "Coconut"; color: "Brown" }
    }
    width: 200
    onCurrentIndexChanged: console.debug(cbItems.get(currentIndex).text + ", " + cbItems.get(currentIndex).color)
}
 */