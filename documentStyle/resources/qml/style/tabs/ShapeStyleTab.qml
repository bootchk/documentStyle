import QtQuick 2.4


import "../controlGroups" as MyControlGroups


Column {
	property string selector: "*.Shape"
	
	MyControlGroups.PenControlGroup {}
	MyControlGroups.BrushControlGroup {}
	MyControlGroups.OpacityControlGroup {}
}