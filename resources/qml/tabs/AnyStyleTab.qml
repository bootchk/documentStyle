import QtQuick 2.3


import "../controlGroups" as MyControlGroups


Column {
	id: anyStyleTabColumn
	
	MyControlGroups.PenControlGroup {
		id: penControlGroup
	}
	MyControlGroups.BrushControlGroup {
		id: brushControlGroup
	}
}