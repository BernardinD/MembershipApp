import 'dart:io';

import 'package:MembershipApp/bloc.navigation_bloc/navigation_bloc.dart';
import 'package:MembershipApp/settingsUtils.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';
import 'package:settings_ui/settings_ui.dart';

import 'package:MembershipApp/main.dart';


class SettingsPage extends StatefulWidget with NavigationStates{
  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool lockInBackground = true;
  bool notificationsEnabled = true;

  // Empty string is a placeholder for temp data
  Map _tempSettings = {'sheet':'', 'email':'', "logo":"", "secret":"", "":null};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Settings UI')),
      body: SettingsList(
        // backgroundColor: Colors.orange,
        sections: [
          SettingsSection(
            title: 'Common',
            // titleTextStyle: TextStyle(fontSize: 30),
            tiles: [
              SettingsTile(
                title: 'Environment',
                subtitle: 'Production',
                leading: Icon(Icons.cloud_queue),
                onTap: () => print('e'),
              ),
            ],
          ),
          SettingsSection(
            title: 'Account',
            tiles: [
              SettingsTile(title: 'Client_secret file', leading: Icon(Icons.insert_drive_file_rounded),
                onTap: (){
                  showDialog(context: context, builder: (BuildContext context){
                    return FileBrowserTile(display:"Choose file", key: "secret", settings: _tempSettings,);
                  });
                },),
              SettingsTile(title: 'Change Spreadsheet', leading: Icon(Icons.phone),
                onTap: (){
                  showDialog(context: context, builder: (BuildContext context){
                    return TextInputTile(display:"Spreadsheet name:", key: "sheet", settings: _tempSettings,);
                  });
                },),
              SettingsTile(title: 'Club Email', leading: Icon(Icons.email),
                onTap: (){
                  showDialog(context: context, builder: (BuildContext context){
                    return TextInputTile(display:"Enter gmail:", key: "email", settings: _tempSettings);
                  });
                },),
              SettingsTile(title: 'Club Name', leading: Icon(Icons.drive_file_rename_outline),
                onTap: (){
                  showDialog(context: context, builder: (BuildContext context){
                    return TextInputTile(display:"Enter Club's name:", key: "club_name", settings: _tempSettings);
                  });
                },),
              SettingsTile(title: 'Create new sheet', leading: Icon(Icons.create_new_folder_rounded),
                onTap: (){
                  showDialog(context: context, builder: (BuildContext context){
                    return TextInputTile(display:"Enter new sheet's name:", key: "", settings: _tempSettings);
                  });
                },),
              /*SettingsTile(
                  title: 'Sign out',
                  leading: Icon(Icons.exit_to_app)
              ),*/
            ],
          ),
          /*SettingsSection(
            title: 'Misc',
            tiles: [
              SettingsTile(
                  title: 'Terms of Service', leading: Icon(Icons.description)),
              SettingsTile(
                  title: 'Open source licenses',
                  leading: Icon(Icons.collections_bookmark)),
            ],
          ),*/
          CustomSection(
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.only(top: 22, bottom: 8),
                  child: Image(
                    image: AssetImage('./iphone-388387_1920.jpg'),
                    width: 150,
                    height: 150,
                  ),
                ),
                Text(
                  'Version: 1.0.0 (287)',
                  style: TextStyle(color: Color(0xFF777777)),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}