import QtQuick 2.3

// model for brush pattern (style)
// No corresponding model in Qt enums?
// [ "Single", "Double", "1.5"] // Must correspond to proportion 100, 150, 200

ListModel {
      ListElement { text: "Single"; value: 100 }
      ListElement { text: "Double"; value: 200 }
      ListElement { text: "1.5"; value: 150 }
}