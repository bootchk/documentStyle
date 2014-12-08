
import QtQuick 2.3
import QtQuick.Dialogs 1.2


ColorDialog {
	title: "Choose color"
	// color is not bound to model, but model initializes it?
	
	// This general dialog is specialized at instantiation with a model
	property var model
	
	
	onAccepted: {
		console.log("You chose: " + color)
		print(currentColor)
		// Qt bug, color is not updated properly, use currentColor
		model.value = currentColor
		model.touched = true
		
		// ??? setting model.value should change model.isReset which is bound to resetButton.enabled???
		// But it doesn't seem to work.  Enable resetButton procedurally
		resetButton.enabled = true
	}
	onRejected: {
		console.log("Canceled")
	}
}