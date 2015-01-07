import QtQuick 2.3

import "../styleSheets" as MyStylesheets

// Specialize:  tool stylesheet is partial (only one tab of a full stylesheet)
MyStylesheets.DelegatedStylesheet{ 
   dialogContentsURL: "../tabs/LineStyleTab.qml" 
   titlePrefix: "Freehand Tool"
   }
