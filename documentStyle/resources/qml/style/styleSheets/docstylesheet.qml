/*
QML for stylesheet editor.

Other notes:
1. stylesheetModel is in root context and is globally referenced
2. other dialogs are owned by components (e.g. style dialog owned by font style control)
3. Whether the 'dialog' is modal, or has  buttons, can be changed later
*/


import QtQuick 2.4

import "../styleSheets" as MyStylesheets

// Specialize it with url of content of dialog node of the tree
// Document stylesheet is full (contrast to DocElementStylesheet which are partial.)
MyStylesheets.DelegatedStylesheet{ 
   dialogContentsURL: "../dialogContents/FullStylesheetContents.qml" 
   titlePrefix: "Doc"
   }