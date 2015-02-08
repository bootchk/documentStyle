import QtQuick 2.4


import "../controlGroups" as MyControlGroups

// Image has only opacity style property

Column {
	property string selector: "*.Pixmap"	// Note not 'Image' see DEType
	
	MyControlGroups.OpacityControlGroup {}
}