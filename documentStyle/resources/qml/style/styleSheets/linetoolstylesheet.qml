import QtQuick 2.4

import "../styleSheets" as MyStylesheets

// Specialize:  tool stylesheet is partial (only one tab of a full stylesheet)
MyStylesheets.DelegatedStylesheet{ 
   dialogContentsURL: "../tabs/LineStyleTab.qml" 
   titlePrefix: "Line Tool"
   }
