import QtQuick 2.1
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1

import UM 1.0 as UM

import "../Preferences"

PreferencesPage {
    //: Machine configuration page title.
    title: qsTr("Machine");

    contents: ColumnLayout {
        anchors.fill: parent;
        RowLayout {
            Label { text: qsTr("Active Machine:"); }
            ComboBox {
                id: machineCombo;
                Layout.fillWidth: true;
                model: UM.Models.machinesModel;
                textRole: "name";
                onCurrentIndexChanged: {
                    if(currentIndex != -1)
                        UM.Models.machinesModel.setActive(currentIndex);
                }

                Connections {
                    id: machineChange
                    target: UM.Application
                    onMachineChanged: machineCombo.currentIndex = machineCombo.find(UM.Application.machineName);
                }

                Component.onCompleted: machineCombo.currentIndex = machineCombo.find(UM.Application.machineName);
            }
            Button { text: qsTr("Remove"); onClicked: confirmRemoveDialog.open(); }
        }
        ScrollView
        {
            Layout.fillWidth: true;
            Layout.fillHeight: true;

            ListView
            {
                delegate: settingDelegate
                model: UM.Models.settingsModel

                section.property: "category"
                section.delegate: Label { text: section }
            }
        }
    }

    Component
    {
        id: settingDelegate
        CheckBox
        {
            text: model.name;
            x: depth * 25
            checked: model.visibility
            onClicked: ListView.view.model.setVisibility(model.key, checked)
            enabled: !model.disabled
        }
    }

    MessageDialog {
        id: confirmRemoveDialog;

        icon: StandardIcon.Question;
        title: qsTr("Confirm Machine Deletion");
        text: qsTr("Are you sure you wish to remove the machine?");
        standardButtons: StandardButton.Yes | StandardButton.No;

        onYes: UM.Models.machinesModel.removeMachine(machineCombo.currentIndex);
    }
}
