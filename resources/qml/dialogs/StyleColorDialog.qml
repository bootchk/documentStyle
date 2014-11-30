
import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2


ColorDialog {
	id: colorDialog
	title: "Choose color"
	property var model	// passed
	
	onAccepted: {
		console.log("You chose: " + colorDialog.color)
		print(currentColor)
		// model.
		// Qt bug, color is not updated properly
		model.value = currentColor
		// Resettable 
		model.touched = true
		
		// resetButton.enabled = true
	}
	onRejected: {
		console.log("Canceled")
	}
}