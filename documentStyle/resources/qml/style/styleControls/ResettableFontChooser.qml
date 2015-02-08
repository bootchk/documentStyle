import QtQuick 2.4
import QtQuick.Controls 1.3
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
	spacing: 10
	
	property string text
	property var model
	property string selector
	
	Label {
		text: parent.text
	}
	
	Button {
		id: fontButton
		text: "Choose"
		
		// Dummy property: reset button refers here, as well as directly to model?
		property var value
		
		// Self is indicator: self.font match chosen font.
		
		style: ButtonStyle {
			label: Text {
        		renderType: Text.NativeRendering
        		verticalAlignment: Text.AlignVCenter
        		horizontalAlignment: Text.AlignHCenter
        		font: model.value
        		text: control.text
      			}
		   }
		
		property var myDialog: MyDialogs.StyleFontDialog {
			id: fontDialog
			model: stylesheetModel.selectResettableValueByStringSelector("*.*.Character.Font")
		}
		
		onClicked: {
			print("font button clicked")
			// Accept actions built into the dialog, except for resetButton.enabled?
			// TODO init view similar to colorchooser?
			fontDialog.open()
		}
	}

	MyControls.ResetButton {
		id: resetButton
		model: parent.model
		buddyControl: fontButton
	}
}

/*
CRUFT when button itself was not an indicator
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
*/