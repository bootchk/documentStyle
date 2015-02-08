import QtQuick 2.4
import QtQuick.Controls 1.3

import "../tabs" as MyTabs


// Style dialog contents is tabbed.

TabView {
	anchors.left: parent.left
	width: 500
	height: 500
	/*
	 * This is cruft trying to get the dialog not to cut off contents
	 * invalid: Layout.fillWidth: true
	anchors.leftMargin: 5;
	anchors.top: parent.top;
	anchors.topMargin: 5;
	
	width: parent.width - 10;
	height: parent.height - 10;
	*/
	
    Tab {
        title: "Any"
        MyTabs.AnyStyleTab {}
    }
    Tab {
        title: "Line"
        MyTabs.LineStyleTab {}
    }
    Tab {
        title: "Shape"
        MyTabs.ShapeStyleTab {}
    }
    Tab {
		title: "Text"
		MyTabs.TextStyleTab {}
	}
	Tab {
		title: "Image"
		MyTabs.ImageStyleTab {}
	}
}
