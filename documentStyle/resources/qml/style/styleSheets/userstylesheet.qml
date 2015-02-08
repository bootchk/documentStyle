import QtQuick 2.4

import "../styleSheets" as MyStylesheets

// Specialize it with url of content of dialog node of the tree
// Document stylesheet is full (contrast to DocElementStylesheet which are partial.)
MyStylesheets.DelegatedStylesheet{ 
	dialogContentsURL: "../dialogContents/FullStylesheetContents.qml"
	titlePrefix: "User"
	}