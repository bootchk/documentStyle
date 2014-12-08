import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

/*
 * A button that resets a buddy control
 * A model is shared between buddy control and this reset button.
 * Model is resettable.
 * 
	We do not need to update view from model here, buddy.value is bound to the model?
 */
Button {
	// Generalized.  Made specific on instantiation.
	property var model
	property var buddyControl
	
	// TODO icon
	text: "Reset"
	
	// Bind to model
	enabled: ! model.isReset	// model=>view
	
	onClicked: {
		print("Reset button clicked")
		// Reset model
		model.isReset = true	// view=>model
		model.touched = true
		
		/*
		Do this ourselves?
		But isReset = true should change model.value and emit valueChanged to bound buddyControl.value
		*/
		buddyControl.value = model.value	// model=>view
		print("model.value", model.value)
		
		/*
		Button state.
		Again, this is bound to model.isReset, which should emit isResetChanged.
		But do it anyway.
		*/
		enabled = false
		
		// Ensure
		console.assert(! enabled, "Assertion failed: reset button disabled.")
		console.assert(model.touched)
		console.assert(buddyControl.value == model.value, "Assertion failed: view == model")
		console.assert(model.isReset, "Assertion failed: model of reset button is reset")
	}
}

