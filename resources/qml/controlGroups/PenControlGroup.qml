import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls

/*
Group of controls for pen.

This is the comment-template for other groups: most comments are here.
*/
GroupBox {
	id: penGroup
	title: "Pen"
	flat: true
	property string selector: parent.selector + ".Pen"

	// A GroupBox is a container, but items are not laid out unless we specify Column
	 Column {
	// ColumnLayout {
		// ??? This causes buttons to obscure content
		// minimumWidth: 200
		spacing: 10
		
		
		StyleControls.ResettableSpinBox {
			text: "Width"
			selector: penGroup.selector + ".Width"
			// Model is part of larger model
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
			//OLD model: DocAnyAnyPenWidth
			// Layout.fillWidth: true
			
			Component.onCompleted: {
				print(x, y, width, height)
				console.assert(typeof stylesheetModel != 'undefined', "stylesheetModel is undefined")
				print(model)
				print(model.value)
			}
		}
		
		StyleControls.ResettableColorChooser {
			text: "Color"
			selector: penGroup.selector + ".Color"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
			Component.onCompleted: {
				print("Completed ResettableColorChooser")
				print(x, y, width, height)
				console.assert(typeof stylesheetModel != 'undefined', "stylesheetModel is undefined")
				print(model)
				print(model.value)
			}
		}
		/* CRUFT
		StyleControls.MyColorChooser {
		}
		*/
		
		StyleControls.ResettableSpinBox {
			text: "Style"
			selector: penGroup.selector + ".Style"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
		}
	}
}	