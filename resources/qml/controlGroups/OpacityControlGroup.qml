import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls

// Group of controls for Opacity.
GroupBox {
	id: opacityGroup
	title: "Opacity"
	flat: true
	property string selector: parent.selector + ".Opacity"

	// A GroupBox is a container, but items are not laid out, unless we specify Column
	Column {
		spacing: 10
		
		StyleControls.ResettableSpinBox {
			text: "     "	// Blank label of proper length, rather than show Opacity:Opacity
			selector: opacityGroup.selector + ".Opacity"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
		}
	}
}	