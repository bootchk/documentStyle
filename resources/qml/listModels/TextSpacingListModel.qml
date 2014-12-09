import QtQuick 2.3

// model for brush pattern (style)
// No corresponding model in Qt enums?
// [ "Single", "Double", "1.5"] // Must correspond to proportion 100, 150, 200

ListModel {
      // OLD, mapped to Qt instrument values of 100, 200, 150
      // NEW map to a contiguous enum
      ListElement { text: "Single"; value: 0 }
      ListElement { text: "Double"; value: 1 }
      ListElement { text: "1.5"; value: 2 }
}