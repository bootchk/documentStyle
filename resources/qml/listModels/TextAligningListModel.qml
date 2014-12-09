import QtQuick 2.3

// model for brush pattern (style)
// Must correspond to Qt.AlignmentFlag 1,2,4,8
// These are horizontal alignments!!!

ListModel {
	// OLD map to Qt values such as Qt.AlignLeft
	// NEW map to contiguous enum
  ListElement { text: "Left"; value: 0 }
  ListElement { text: "Right"; value: 1 }
  ListElement { text: "Center"; value: 2 }
  ListElement { text: "Justify"; value: 3 }
}