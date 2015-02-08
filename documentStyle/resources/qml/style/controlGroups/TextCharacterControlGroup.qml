import QtQuick 2.4
import QtQuick.Controls 1.3

import "../styleControls" as StyleControls


// Group of controls for Brush.
GroupBox {
	id: characterGroup
	title: "Character"
	flat: true
	property string selector: parent.selector + ".Character"

	 Column {
		spacing: 10
		
		StyleControls.ResettableFontChooser {
			text: "Font"
			selector: characterGroup.selector + ".Font"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
		}
		
		StyleControls.ResettableColorChooser {
			text: "Color"
			selector: characterGroup.selector + ".Color"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
		}
		
		
	}
}	