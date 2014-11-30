import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1


import "../tabs" as MyTabs

//ColumnLayout {
TabView {
	// invalid: Layout.fillWidth: true
	anchors.left: parent.left;
	width: 500
	height: 500
	/*
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
        MyTabs.AnyStyleTab {}
    }
    Tab {
        title: "Shape"
        MyTabs.AnyStyleTab {}
    }
    Tab {
		title: "Text"
		MyTabs.AnyStyleTab {}
	}
	Tab {
		title: "Image"
		MyTabs.AnyStyleTab {}
	}
}
//}
