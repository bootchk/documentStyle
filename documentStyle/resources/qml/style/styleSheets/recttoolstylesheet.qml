import QtQuick 2.3

import "../styleSheets" as MyStylesheets

// Specialize:  tool stylesheet is partial (only one tab of a full stylesheet)
MyStylesheets.DelegatedStylesheet{ 
   dialogContentsURL: "../tabs/ShapeStyleTab.qml" 
   titlePrefix: "Rect Tool"
   }
