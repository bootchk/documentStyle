
import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Dialogs 1.2

// See comments in StyleColorDialog.qml

FontDialog {
	id: fontDialog
	title: "Choose font"
	property var model	// passed
	
	onAccepted: {
		console.log("You chose: " + font)
		console.assert(font == currentFont)
		model.value = currentFont
		model.touched = true
		
		resetButton.enabled = true
	}
	onRejected: {
		console.log("Canceled")
	}
}