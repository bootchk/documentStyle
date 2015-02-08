import QtQuick 2.4

// model for pen pattern (style)
// Must correspond to Qt.PenStyle

ListModel {
      ListElement { text: "Invisible"; value: 0 }
      ListElement { text: "Solid"; value: 1 }
      ListElement { text: "Dash"; value: 2 }
      ListElement { text: "Dot"; value: 3 }
      ListElement { text: "DashDot"; value: 4 }
}
