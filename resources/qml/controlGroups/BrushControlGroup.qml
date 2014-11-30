import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls

/*
Group of controls for Brush.
*/
GroupBox {
		id: brushGroup
		title: "Brush"
		flat: true

	// A GroupBox is a container, but items are not laid out.
	 Column {
		id: layout
		spacing: 10
		
		StyleControls.ResettableColorChooser {
			id: myAnyBrushColorChooser
			text: "Color"
			model: DocAnyAnyBrushColor
		}
		
		StyleControls.ResettableSpinBox {
			id: docAnyAnyBrushStyle
			text: "Style"
			model: DocAnyAnyBrushStyle
		}
	}
}	