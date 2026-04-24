// SPDX-FileCopyrightText: 2024 Open Mobile Platform LLC <community@omp.ru>
// SPDX-License-Identifier: BSD-3-Clause

import QtQuick 2.0
import Sailfish.Silica 1.0

Page {
    objectName: "errorPage"

    property alias errorMessage: errorMessageLabel.text

    PageHeader {
        id: pageHeader

        objectName: "pageHeader"
        title: qsTr("Error page")
    }

    Column {
        objectName: "infoColumn"
        anchors {
            top: pageHeader.bottom
            left: parent.left
            right: parent.right
            margins: Theme.horizontalPageMargin
        }
        spacing: Theme.paddingMedium

        Label {
            anchors {
                left: parent.left
                right: parent.right
            }
            text: qsTr("An error has occurred")
        }

        Label {
            id: errorMessageLabel

            anchors {
                left: parent.left
                right: parent.right
            }
            wrapMode: Text.Wrap
        }
    }
}
