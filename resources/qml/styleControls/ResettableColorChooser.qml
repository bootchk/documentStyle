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
	
	Label {
		id: label
		text: parent.text
	}
	
	// This doesn't work:    width: theme.itemSizeSmall
	Rectangle {
	    id: colorIndicator
	    color: model.value
	    // resetButton references colorIndicator.value
	    property alias value: colorIndicator.color
	    visible: true
	    width: parent.height - 2	// theme.itemSizeSmall
	    height: parent.height - 2	//40	// theme.itemSizeSmall
	}
	
	Button {
		id: colorButton
		text: "Choose"
		// This doesn't work
		style: ButtonStyle {
		        background: Rectangle {
		        	color: colorDialog.currentColor
		            implicitWidth: 100
		            implicitHeight: 25
		            border.width: control.activeFocus ? 2 : 1
		            border.color: "#888"
		            radius: 4
		            gradient: Gradient {
		                GradientStop { position: 0 ; color: control.pressed ? "#ccc" : "#eee" }
		                GradientStop { position: 1 ; color: control.pressed ? "#aaa" : "#ccc" }
		            }
		        }
		    }
		// color: colorDialog.color
		onClicked: {
			print("color button clicked")
			colorDialog.accepted.connect(function() {
		            // No need, is bound: colorIndicator.color = colorDialog.currentColor
		            // label.color = colorDialog.currentColor
		            model.value = colorDialog.currentColor	// side effect should be enabling of reset button?
		            model.touched = true
		            // This is not allowed by model: model.isReset = false
		            // The above setting of model.value does not seem to have proper side effect, so do it here.
		            resetButton.enabled = true
		        })
			colorDialog.open()
		}
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: colorIndicator
	}
	
	/*
	Button {
		id: resetButton
		text: "Reset"
		// bind enable to model
		enabled: ! model.isReset
		onClicked: {
			print("Color reset button clicked")
			// Reset model
			model.isReset = true	// Side effect is model.value changes and valueChanged emitted
			model.touched = true
			// colorIndicator.color = model.value	// Do this ourselves, instead of from signal from model
			// Assert view value is reset also
			print("model.value", model.value)
			// Button state
			enabled = false
		}
	}
	*/
}
