import QtQuick 2.3
import QtQuick.Controls 1.2

import "../styleControls" as StyleControls
import "../listModels" as ListModels

// Group of controls for Brush.
GroupBox {
	id: brushGroup
	title: "Brush"
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