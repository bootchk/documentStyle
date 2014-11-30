import QtQuick 2.3


import "../controlGroups" as MyControlGroups


Column {
	id: lineStyleTabColumn
	
	MyControlGroups.PenControlGroup {}
	
	// Qt Line really has a Brush, but we omit
	
	MyControlGroups.OpacityControlGroup {}
}