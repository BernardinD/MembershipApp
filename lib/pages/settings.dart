import 'package:MembershipApp/bloc.navigation_bloc/navigation_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';
import 'package:settings_ui/settings_ui.dart';

import 'package:MembershipApp/main.dart';


class SettingsPage extends StatefulWidget with NavigationStates{
  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class TextInputTile extends StatefulWidget{
  String _display, _key;
  Map _settings;
  TextInputTile({String display, String key, Map settings}){_display = display; _key = key; _settings = settings;}

  @override
  _TextInputTileState createState() => _TextInputTileState(_display, _key, _settings);
}

class _TextInputTileState extends State<TextInputTile> {

  String _display, _key, _new;
  Map _settings;
  _TextInputTileState(String display, String key, Map settings){_display=display; _key=key; _settings=settings;}

  final formKey = GlobalKey<FormState>();
  void _submit(String key){
    debugPrint("_settings[_key] = " + _settings.toString());
    if(formKey.currentState.validate()){
      formKey.currentState.save();
        MyApp.prefs.setString(key, _settings[_key]);
        Navigator.pop(context);
        debugPrint("New value: ${MyApp.prefs.getString(_key)}");
    }
  }
  @override
  Widget build(BuildContext content) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return AlertDialog(
      content: Container(
        height: screenHeight*0.25,
        alignment: Alignment.center,
        child:
          Form(
            key: formKey,
            child: Column(
                children: <Widget>[
                  TextFormField(
                    decoration: InputDecoration(
                        labelText: "Current: ${MyApp.prefs.getString(_key??"") ?? "N/A"} "
                    ),
                    enabled: false,
                    // validator: (input) => input.length < 1 ? 'Not a valid Email' : null,
                    // onSaved: (input) => _settings[_key] = input,
                  ),
                  TextFormField(
                    decoration: InputDecoration(
                        labelText: _display
                    ),
                    validator: (input) => input.length < 1 ? 'Not a valid Email' : null,
                    onSaved: (input) => _settings[_key] = input,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Padding(
                        padding: const EdgeInsets.fromLTRB(4.0, 3, 8, 0),
                        child: RaisedButton(
                          onPressed: () => _submit(_key),
                          child: Text('Submit'),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.fromLTRB(8.0, 3, 4, 0),
                        child: RaisedButton(
                          onPressed: () =>  Navigator.pop(content),
                          child: Text('Cancel'),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
          ),
      )
    );
  }
}

class _SettingsPageState extends State<SettingsPage> {
  bool lockInBackground = true;
  bool notificationsEnabled = true;
  Map _tempSettings = {'sheet':'', 'email':''};

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
                    return TextInputTile(display:"Enter new sheet's name:", key: "");
                  });
                },),
              SettingsTile(
                  title: 'Sign out',
                  leading: Icon(Icons.exit_to_app)
              ),
            ],
          ),
          SettingsSection(
            title: 'Security',
            tiles: [
              SettingsTile.switchTile(
                title: 'Lock app in background',
                leading: Icon(Icons.phonelink_lock),
                switchValue: lockInBackground,
                onToggle: (bool value) {
                  setState(() {
                    lockInBackground = value;
                    notificationsEnabled = value;
                  });
                },
              ),
              SettingsTile.switchTile(
                  title: 'Use fingerprint',
                  leading: Icon(Icons.fingerprint),
                  onToggle: (bool value) {},
                  switchValue: false),
              SettingsTile.switchTile(
                title: 'Change password',
                leading: Icon(Icons.lock),
                switchValue: true,
                onToggle: (bool value) {},
              ),
              SettingsTile.switchTile(
                title: 'Enable Notifications',
                enabled: notificationsEnabled,
                leading: Icon(Icons.notifications_active),
                switchValue: true,
                onToggle: (value) {},
              ),
            ],
          ),
          SettingsSection(
            title: 'Misc',
            tiles: [
              SettingsTile(
                  title: 'Terms of Service', leading: Icon(Icons.description)),
              SettingsTile(
                  title: 'Open source licenses',
                  leading: Icon(Icons.collections_bookmark)),
            ],
          ),
          CustomSection(
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.only(top: 22, bottom: 8),
                  child: Image.asset(
                    'assets/settings.png',
                    height: 50,
                    width: 50,
                    color: Color(0xFF777777),
                  ),
                ),
                Text(
                  'Version: 2.4.0 (287)',
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