import QtQuick 2.4
import QtQuick.Controls 1.3

import "../styleControls" as StyleControls

// Group of controls for Opacity.
GroupBox {
	id: opacityGroup
	title: "Opacity"
	flat: true
	property string selector: parent.selector + ".Opacity"

	Column {
		spacing: 10
		
		StyleControls.ResettableSpinBox {
			text: "     "	// Blank label of proper length, rather than show Opacity:Opacity
			selector: opacityGroup.selector + ".Opacity"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
			
			// Specialize to float control
			controlDecimals: 1
			controlStepSize: 0.1
			controlMinimumValue: 0.1	// So user can't make it invisible
			controlMaximumValue: 1.0
		}
	}
}	