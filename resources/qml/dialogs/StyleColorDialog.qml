
import QtQuick 2.3
import QtQuick.Dialogs 1.2


ColorDialog {
	title: "Choose color"
	// This general dialog is specialized at instantiation with a model
	property var model
	
	onAccepted: {
		console.log("You chose: " + color)
		print(currentColor)
		// Qt bug, color is not updated properly, use currentColor
		model.value = currentColor
		model.touched = true
		
		// resetButton.enabled = true ???
	}
	onRejected: {
		console.log("Canceled")
	}
}