import QtQuick 2.4
import QtQuick.Controls 1.3		// for GroupBox

import "../styleControls" as StyleControls
import "../listModels" as ListModels

// Group of controls for Brush.
GroupBox {
	id: brushGroup
	property string role: ""
	title: role + "Brush"
	flat: true
	property string selector: parent.selector + ".Brush"

	 Column {
		spacing: 10
		
		// Style ahead of Color so user sees that Style is None before choosing Color
		StyleControls.ResettableComboBox {
					text: "Style"
					selector: brushGroup.selector + ".Style"
					model: stylesheetModel.selectResettableValueByStringSelector(selector)
					domain: ListModels.BrushStyleListModel{}
				}
		
		StyleControls.ResettableColorChooser {
			text: "Color"
			selector: brushGroup.selector + ".Color"
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
		}
	}
}	