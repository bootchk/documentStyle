import QtQuick 2.3

// model for brush pattern (style)
// Must correspond to Qt.AlignmentFlag 1,2,4,8

ListModel {
      ListElement { text: "Left"; value: 1 }
      ListElement { text: "Right"; value: 2 }
      ListElement { text: "Center"; value: 4 }
      ListElement { text: "Justify"; value: 8 }
}