import QtQuick 2.4
import QtQuick.Controls 1.3

import "../styleControls" as StyleControls
import "../listModels" as ListModels


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
			domain: ListModels.TextSpacingListModel{}
		}
		StyleControls.ResettableComboBox {
			text: "Aligning"
			selector: blockGroup.selector + ".Aligned"	// !!! difference
			model: stylesheetModel.selectResettableValueByStringSelector(selector)
			domain: ListModels.TextAligningListModel{}
		}
	}
}	