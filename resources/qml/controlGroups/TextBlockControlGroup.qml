import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls


// Group of controls for Text Block i.e. paragraph?
GroupBox {
	id: blockGroup
	title: "Block"
	flat: true
	property string selector: parent.selector + ".Block"

	 Column {
		spacing: 10
		
		StyleControls.ResettableComboBox {
			text: "Spacing"
			selector: blockGroup.selector + ".Spacing"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
			domain: [ "Single", "Double", "1.5"]	// Must correspond to proportion 100, 150, 200
		}
		StyleControls.ResettableComboBox {
			text: "Aligning"
			selector: blockGroup.selector + ".Aligned"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
			domain: [ "Left", "Right", "Center", "Justify"]	// Must correspond to Qt.AlignmentFlag 1,2,4,8
		}
	}
}	