import QtQuick 2.3


import "../controlGroups" as MyControlGroups


Column {
	property string selector: "*.Shape"
	
	MyControlGroups.PenControlGroup {}
	MyControlGroups.BrushControlGroup {}
	MyControlGroups.OpacityControlGroup {}
}