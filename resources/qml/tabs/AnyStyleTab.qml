import QtQuick 2.3

import "../controlGroups" as MyControlGroups


Column {
	property string selector: "*.*"
	
	MyControlGroups.PenControlGroup {}
	MyControlGroups.BrushControlGroup {}
}