import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls

/*
Group of controls for pen.
*/
GroupBox {
		id: penGroup
		title: "Pen"
		flat: true

	// A GroupBox is a container, but items are not laid out.
	 Column {
	// ColumnLayout {
		id: layout
		// ??? This causes buttons to obscure content
		// minimumWidth: 200
		spacing: 10
		
		StyleControls.ResettableSpinBox {
			id: bar
			text: "Width"
			model: DocAnyAnyPenWidth
			// Layout.fillWidth: true
			
			Component.onCompleted: print(x, y, width, height)
		}
		
		StyleControls.ResettableColorChooser {
			id: myAnyPenColorChooser
			text: "Color"
			model: DocAnyAnyPenColor
		}
		/*
		StyleControls.MyColorChooser {
			id: myAnyPenColorChooser
			model: DocAnyAnyPenColor
		}
		*/
		
		StyleControls.ResettableSpinBox {
			id: docAnyAnyPenStyle
			text: "Style"
			model: DocAnyAnyPenStyle
		}
	}
}	