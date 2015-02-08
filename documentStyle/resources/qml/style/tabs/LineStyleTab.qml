import QtQuick 2.4

import "../controlGroups" as MyControlGroups


Column {
	property string selector: "*.Line"
	
	MyControlGroups.PenControlGroup {}
	// Qt Line really has a Brush, but we omit, users don't want?
	MyControlGroups.OpacityControlGroup {}
}