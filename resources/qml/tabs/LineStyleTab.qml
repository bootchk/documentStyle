import QtQuick 2.3

import "../controlGroups" as MyControlGroups


Column {
	property string selector: "*.Line"
	
	MyControlGroups.PenControlGroup {}
	// Qt Line really has a Brush, but we omit, users don't want?
	MyControlGroups.OpacityControlGroup {}
}