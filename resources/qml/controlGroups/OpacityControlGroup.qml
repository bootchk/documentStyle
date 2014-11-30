import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls

/*
Group of controls for Opacity.
*/
GroupBox {
		title: "Opacity"
		flat: true

	// A GroupBox is a container, but items are not laid out.
	 Column {
		spacing: 10
		
		StyleControls.ResettableSpinBox {
			text: "     "	// Rather than show Opacity:Opacity
			model: DocAnyAnyOpacityOpacity
		}
	}
}	