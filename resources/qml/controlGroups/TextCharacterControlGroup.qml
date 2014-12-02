import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls


// Group of controls for Brush.
GroupBox {
	id: characterGroup
	title: "Character"
	flat: true
	property string selector: parent.selector + ".Character"

	 Column {
		spacing: 10
		
		// TODO FontChooser
		StyleControls.ResettableComboBox {
					text: "Font"
					selector: characterGroup.selector + ".Font"
					model: stylesheetModel.selectResettableValueByStringSelector(selector)
					domain: [ "None", "Solid", "Dense1", "Dense2", "Dense3"]	// Must correspond to Qt.PenStyle
				}
		
		StyleControls.ResettableColorChooser {
			text: "Color"
			selector: characterGroup.selector + ".Color"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
		}
		
		
	}
}	