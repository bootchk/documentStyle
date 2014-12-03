import QtQuick 2.3

// model for brush pattern (style)
// Must correspond to Qt.AlignmentFlag 1,2,4,8
// These are horizontal alignments!!!

ListModel {
      ListElement { text: "Left"; value: Qt.AlignLeft }
      ListElement { text: "Right"; value: Qt.AlignRight }
      ListElement { text: "Center"; value: Qt.AlignHCenter }
      ListElement { text: "Justify"; value: Qt.AlignJustify }
}