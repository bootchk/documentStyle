import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2

import "../styleControls" as MyControls
import "../dialogs" as MyDialogs

/*
 See: ResettableSpinBox which is the commented template for this.
 This is the equivalent of a QWidget.
 See also ResettableColorChooser which has similarities.
 
 Note GUI design problem: feeding back a large font choice without disturbing the layout of this control.
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
	Label {
	    id: fontIndicator
	    text: "Current font"
	    font: model.value
	    // resetButton references Indicator.value
	    property alias value: fontIndicator.font
	    //visible: true
	    //width: parent.height - 2	// theme.itemSizeSmall
	    //height: parent.height - 2	//40	// theme.itemSizeSmall
	}
	
	Button {
		id: fontButton
		text: "Choose"
		/*
		 * Set color of self to match chosen color.
		 * This doesn't work
		 style: ButtonStyle {
		        see ColorChooser
		 */
		// Button has no color property...   color: colorDialog.color
		
		property var myDialog: MyDialogs.StyleFontDialog {
			id: fontDialog
			model: stylesheetModel.selectResettableValueByStringSelector("*.*.Character.Font")
		}
		
		onClicked: {
			print("font button clicked")
			// Accept actions built into the dialog, except for resetButton.enabled?
			fontDialog.open()
		}
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: fontIndicator
	}
}
