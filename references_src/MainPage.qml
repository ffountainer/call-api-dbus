// SPDX-FileCopyrightText: 2024 Open Mobile Platform LLC <community@omp.ru>
// SPDX-License-Identifier: BSD-3-Clause

import QtQuick 2.0
import Sailfish.Silica 1.0
import ru.auroraos.CallApiDBus 1.0

Page {
    id: root

    objectName: "mainPage"

    CallManager {
        id: appCallManager
    }

    onStatusChanged: {
        if (status === PageStatus.Active)
            controller.registerCallManager();
    }

    MainPageController {
        id: controller

        callManager: appCallManager
        onCallManagerErrorReceived: pageStack.push(Qt.resolvedUrl("ErrorPage.qml"), {
            "errorMessage": errorMessage
        })

        onDtmfStringChanged: {
            dtmfTextArea.text = controller.dtmfString;
        }
    }

    PageHeader {
        id: pageHeader

        objectName: "pageHeader"
        title: qsTr("Call API DBus")
        extraContent.children: [
            IconButton {
                objectName: "aboutButton"
                icon.source: "image://theme/icon-m-about"
                anchors.verticalCenter: parent.verticalCenter
                onClicked: pageStack.push(Qt.resolvedUrl("AboutPage.qml"))
            }
        ]
    }

    Column {
        id: mainColumn

        objectName: "buttonsColumn"
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: Theme.horizontalPageMargin
            rightMargin: Theme.horizontalPageMargin
            verticalCenter: parent.verticalCenter
        }
        spacing: Theme.paddingLarge

        Timer {
            id: incomingTimer
            property int secsLeft: 5

            interval: 1000
            repeat: true
            onTriggered: {
                secsLeft -= 1;
                if (secsLeft === 0) {
                    controller.startIncomingCall();
                    incomingTimer.stop();
                    secsLeft = 5;
                }
            }
        }

        SectionHeader {
            text: qsTr("Calls")
        }

        Button {
            objectName: "outgoingCallButton"
            enabled: !incomingTimer.running

            width: parent.width

            text: qsTr("Outgoing call")

            onClicked: controller.startOutgoingCall()
        }

        Button {
            objectName: "incomingCallButton"

            width: parent.width
            enabled: !incomingTimer.running
            text: qsTr("Incoming call") + (incomingTimer.running ? " (%1)".arg(incomingTimer.secsLeft) : "")

            onClicked: incomingTimer.start()
        }

        SectionHeader {
            text: qsTr("Functions")
        }

        TextSwitch {
            id: holdableModeSwitch

            width: parent.width
            enabled: !incomingTimer.running

            text: qsTr("Hold")

            description: qsTr("On/Off the call hold mode")

            onCheckedChanged: {
                controller.setHoldableMode(checked);
            }
        }


        TextSwitch {
            id: dtmfStateSwitch

            width: parent.width
            enabled: !incomingTimer.running

            text: qsTr("DTMF")

            description: qsTr("On/Off DTMF(support numeric keyboard)")

            onCheckedChanged: {
                controller.setDtmf1Enabled(checked);
            }
        }
    }

    TextArea {
        id: dtmfTextArea

        anchors.top: mainColumn.bottom

        width: parent.width
        height: 200

        visible: dtmfStateSwitch.checked

        anchors.margins: Theme.paddingMedium

        text: ""
        placeholderText: qsTr("DTMF text")

        readOnly: true

        color: Theme.primaryColor
        placeholderColor: Theme.secondaryColor

        wrapMode: Text.Wrap
    }
}
