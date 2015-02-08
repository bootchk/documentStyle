import QtQuick 2.4

import "../styleSheets" as MyStylesheets

// Specialize
// DocumentElement stylesheet is partial (only one tab of a full stylesheet)
MyStylesheets.DelegatedStylesheet{ 
   dialogContentsURL: "../tabs/TextStyleTab.qml" 
   titlePrefix: "Text"
   }
