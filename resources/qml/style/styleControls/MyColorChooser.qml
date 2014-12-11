import QtQuick 2.3
// import QtQuick.Controls 1.2

import "../dialogs" as MyDialogs
import "../styleControls" as StyleControls


Item {
	id: myColorChooser
	property var model	// passed
	
	StyleControls.ResettableColorChooser {
		id: baz
		text: "Color"
		model: parent.model
	}
	
	
}