import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.2

import "../styleControls" as MyControls
import "../dialogs" as MyDialogs

/*
 See: ResettableSpinBox which is the commented template for this.
 This is the equivalent of a QWidget.
*/ 
Row {
	spacing: 10

	property string text
	property var model
	property string selector
	
	// chooser dialog owned by this control, specialized with model
	property var chooserDialog: MyDialogs.StyleColorDialog {
		model: stylesheetModel.selectResettableValueByStringSelector(selector)
	}
	
	Label {
		text: parent.text
	}
	
	Button {
		id: colorButton
		text: "Choose"
		
		/* 
		Dummy property: reset button refers here, as well as directly to model?
		
		I also tried these:
		// TODO this makes reset button not enabled
		//property var color: model.value
		// Alias color since resetButton resets 'value'
		//property alias value: colorButton.color
		//property var value: model.value
		*/
		property var value
		
		
		style: ButtonStyle {
		        background: Rectangle {
		        	/*
		        	Fails if bind color to chooserDialog.color instead of currentColor
		        	Should be bound to model, not chooserDialog, anyway.
		        	*/
		        	color: model.value
		        	
		            implicitWidth: 100
		            implicitHeight: 25
		            border.width: control.activeFocus ? 2 : 1
		            border.color: "#888"
		            radius: 4
		            /*
		            Fails to show model.color if this is uncommented?
		            gradient: Gradient {
		                GradientStop { position: 0 ; color: control.pressed ? "#ccc" : "#eee" }
		                GradientStop { position: 1 ; color: control.pressed ? "#aaa" : "#ccc" }
		            }
		            */
		        }
		    }
		
		onClicked: {
			print("color button clicked")
			// chooserDialog knows model and changes it onAccepted
			
			// Initialize dialog's view from model, it is not bound
			chooserDialog.color = model.value	// color works, currentColor fails to init
			
			// print("color chooser:", chooserDialog.currentColor)
			chooserDialog.open()
		}
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: colorButton	// colorIndicator
	}
}

/* CRUFT: when button itself did not indicate the chosen color
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
	*/