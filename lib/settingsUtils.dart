import 'package:MembershipApp/main.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as path;

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

    debugPrint("MyApp.prefs.getString('${_key}') = ${MyApp.prefs.getString(_key)}");
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
                      padding: const EdgeInsets.fromLTRB(4.0, 0, 8, 0),
                      child: RaisedButton(
                        onPressed: () => _submit(_key),
                        child: Text('Submit'),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(8.0, 0, 4, 0),
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

class FileBrowserTile extends StatefulWidget{
  String _display, _key;
  Map _settings;
  FileBrowserTile({String display, String key, Map settings}){_display = display; _key = key; _settings = settings;}

  @override
  _FileBrowserTileState createState() => _FileBrowserTileState(_display, _key, _settings);
}

class _FileBrowserTileState extends State<FileBrowserTile> {

  String _display, _key, _new;
  Map _settings;
  _FileBrowserTileState(String display, String key, Map settings){_display=display; _key=key; _settings=settings;}

  final formKey = GlobalKey<FormState>();



  String _fileName;
  List<PlatformFile> _paths;
  String _directoryPath;
  String _extension = "json";
  bool _loadingPath = false;
  bool _multiPick = false;
  FileType _pickingType = FileType.custom;
  TextEditingController _controller = TextEditingController();

  Future _openFileExplorer() async {
    setState(() => _loadingPath = true);
    try {
      _directoryPath = null;
      _paths = (await FilePicker.platform.pickFiles(
        type: _pickingType,
        allowMultiple: _multiPick,
        allowedExtensions: (_extension?.isNotEmpty ?? false)
            ? _extension?.replaceAll(' ', '')?.split(',')
            : null,
      ))
          ?.files;

      return _paths[0];

    } on PlatformException catch (e) {
      print("Unsupported operation" + e.toString());
    } catch (ex) {
      print(ex);
    }
    if (!mounted) return;
    setState(() {
      _loadingPath = false;
      _fileName = _paths != null ? _paths.map((e) => e.name).toString() : '...';
    });
  }

  void _submit(String key){
    debugPrint("_settings[_key] = " + _settings.toString());
    if(formKey.currentState.validate()){
      formKey.currentState.save();
      MyApp.prefs.setString(key, _paths[0].path.toString());
      Navigator.pop(context);
      debugPrint("New value: ${MyApp.prefs.getString(_key)}");
    }
  }
  @override
  Widget build(BuildContext content) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    debugPrint("MyApp.prefs.getString('${_key}') = ${MyApp.prefs.getString(_key)}");
    return AlertDialog(
        content: Container(
          height: screenHeight*0.25,
          alignment: Alignment.center,
          child:
          Form(
            key: formKey,
            child: Column(
              children: <Widget>[
                // TextFormField(
                //   decoration: InputDecoration(
                //       labelText: "Current: ${path.basename(MyApp.prefs.getString(_key??"")) ?? "N/A"} "
                //   ),
                //   enabled: false,
                //   // validator: (input) => input.length < 1 ? 'Not a valid Email' : null,
                //   // onSaved: (input) => _settings[_key] = input,
                // ),
                TextFormField(
                  controller: _controller,
                  decoration: InputDecoration(
                      labelText: _display
                  ),
                  enabled: false,
                  validator: (input) => input.length < 1 ? 'Not a valid Email' : null,
                  onSaved: (input) => _settings[_key] = _paths[0].path,
                ),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Padding(
                      padding: const EdgeInsets.fromLTRB(4.0, 3, 8, 0),
                      child: RaisedButton(
                        onPressed: () => _openFileExplorer().then((path){
                          _controller.text = path.name;
                        }),
                        child: Text('Browse'),
                      ),
                    ),
                    ],
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
