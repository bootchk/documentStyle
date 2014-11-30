import QtQuick 2.3
import QtQuick.Controls 1.2
//import QtQuick.Dialogs 1.2
import QtQuick.Controls.Styles 1.2

// import People 1.0

/*
 
See:
	-userInterface.resettableControls.spinBox.py
	-userInterface.layout.stylePropertyLayout.py
which are the QWidget version of this QML.

Row:  [label, control, reset button]

The reset button resets the control.
*/ 
Row {
	// Passed at instantiation
	property string text // label.text bound here
	property var model
	
	Label {
		id: label
		text: parent.text
	}
	
	// This doesn't work:    width: theme.itemSizeSmall
	Rectangle {
	    id: colorIndicator
	    color: "red"
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
			/*
			Sailfish
			var dialog = pageStack.push("ColorDialog")
		    dialog.accepted.connect(function() {
		            colorIndicator.color = dialog.color
		        })
		    */
			colorDialog.accepted.connect(function() {
		            colorIndicator.color = colorDialog.currentColor
		            label.color = colorDialog.currentColor
		        })
			colorDialog.open()
		}
	}

	Button {
		/*
		Model is resettable.
		We do not need to update view from model now,
		spinBox.value is bound to the model.
		*/
		id: resetButton
		text: "Reset"
		// enable according to model TODO
		enabled: false
		onClicked: {
			print("button clicked")
			// Reset model
			model.isReset = true
			model.touched = true
			spinbox.value = model.value	// Do this ourselves, instead of from signal from model
			// Assert view value is reset also
			print("model.value", model.value)
			// Button state
			enabled = false
		}
	}
}