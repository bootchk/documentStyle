import QtQuick 2.3

import "../controlGroups" as MyControlGroups


Column {
	property string selector: "*.Text"
	
	MyControlGroups.TextCharacterControlGroup {} 
	MyControlGroups.TextBlockControlGroup {}
	MyControlGroups.PenControlGroup {}	// role:Frame}
	MyControlGroups.BrushControlGroup {}	//role:Ground}
	MyControlGroups.OpacityControlGroup {}
}