import QtQuick 2.3


import "../controlGroups" as MyControlGroups


Column {
	property string selector: "*.Text"
	
	//MyControlGroups.CharacterControlGroup {} 
	//MyControlGroups.BlockControlGroup {}
	MyControlGroups.PenControlGroup {}	// Frame
	MyControlGroups.BrushControlGroup {}	// Ground
	MyControlGroups.OpacityControlGroup {}
}