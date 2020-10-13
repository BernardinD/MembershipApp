import 'dart:io';
import 'dart:typed_data';
import 'dart:ui';

import 'package:MembershipApp/main.dart';
import 'package:email_validator/email_validator.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:googleapis_auth/auth_io.dart';
import 'package:gsheets/gsheets.dart';
import 'package:mailto/mailto.dart';
import 'package:path_provider/path_provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../bloc.navigation_bloc/navigation_bloc.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:googleapis/drive/v3.dart' as drive;

import '../driveUtils.dart';

class AddMemberPage extends StatefulWidget with NavigationStates {
  @override
  AddMemberPageState createState() => new AddMemberPageState();
}

class AddMemberPageState extends State<AddMemberPage>  {
  final formKey = GlobalKey<FormState>();
  String _first, _last, _email, _phone, _data ="";
  bool _confirmEnabled = false, _submitEnabled = true;
  String folderID;

  // Used for controlling when to take screenshot
  GlobalKey globalKey = new GlobalKey();

  // Use this controller to clear all text fields
  TextEditingController _controller = TextEditingController();

  // final pattern = r'^[0-9]{3}\s?[0-9]{3}\s?[0-9]{4}$';
  final regExp = RegExp(r'^[0-9]{3}\s?[0-9]{3}\s?[0-9]{4}$');

  @override
  void initState() {
    super.initState();

    // Initialize everything needs to spreadsheet
    Utils.getSpread(context, "Testing").then((spread) {
      print("Final result: " + spread.toString());
    });

    // Initialize folders
    List<String> names = ["Testing", "2020"];
    Utils.findFolders(context, "Testing", "2020").then((folders) async {
      String prevID = "root";
      int i = 0;
      for(var folder in folders){
        if (folder == null){
          await Utils.createFolders(context, names[i++], prevID);
        }
        else{
          prevID = folder.id;
        }
      }
      folderID = prevID;
    });

  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
          children: <Widget>[
            Text(
              "Add Member Page",
              style: TextStyle(fontWeight: FontWeight.w900, fontSize: 28),
            ),
            Card(
              child: Padding(
                padding: EdgeInsets.all(8.0),
                child: Form(
                  key: formKey,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                    RepaintBoundary(
                      key: globalKey,
                      child: QrImage(
                        data: _data,
                        version: QrVersions.auto,
                        size: 220,
                        gapless: false,
                      ),
                    ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: <Widget>[
                          Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: RaisedButton(
                              onPressed: () => setState(() {
                                formKey.currentState.reset();
                                FocusScope.of(context).unfocus();
                                _confirmEnabled = false;
                                _submitEnabled = true;
                                _first = _last = _email = _phone = "Testing123";
                                _data = "";
                              }),
                              child: Text('Reset'),
                              autofocus: true,
                            ),
                          ),
                        ],
                      ),
                      TextFormField(
                        decoration: InputDecoration(
                            labelText: 'First name:'
                        ),
                        validator: (input) => input.length < 2 ? 'You need at least 2 characters' : null,
                        onSaved: (input) => _first = input.trim(),
                      ),
                      TextFormField(
                        decoration: InputDecoration(
                            labelText: 'Last name:'
                        ),
                        validator: (input) => input.length < 2 ? 'You need at least 2 characters' : null,
                        onSaved: (input) => _last = input.trim(),
                        // obscureText: true,
                      ),
                      TextFormField(
                        decoration: InputDecoration(
                            labelText: 'Email:'
                        ),
                        validator: (input) => EmailValidator.validate(input) ? null : 'Not a valid Email',
                        onSaved: (input) => _email = input.trim(),
                      ),
                      TextFormField(
                        decoration: InputDecoration(
                            labelText: 'Phone number (XXX XXX XXXX):'
                        ),
                        validator: (input) => regExp.hasMatch(input) ? null : 'Not a valid number. Make sure there are 10 digits',
                        onSaved: (input) => _phone = input.trim(),
                        // obscureText: true,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: <Widget>[
                          Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: RaisedButton(
                              onPressed: _submitEnabled ? () => setState(() => _submit()) : null,
                              child: Text('Submit'),
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: RaisedButton(
                              onPressed: _confirmEnabled ? () =>  _confirm() : null,
                              child: Text('Confirm'),
                            ),
                          ),
                        ],
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: <Widget>[
                          Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: RaisedButton(
                              onPressed: (Utils.webLink != null) ? () async { if (await canLaunch(Utils.webLink)) await launch(Utils.webLink);}  : null,
                              child: Text('Open Spreadsheet'),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ]
      ),
    );
  }

  void _submit(){
    if(formKey.currentState.validate()){
      print(_first);
      print(_last);
      print(_email);
      print(_phone);
      _confirmEnabled = true;
      _submitEnabled = false;
    }
  }
  void _confirm(){
    formKey.currentState.save();
    print(_first);
    print(_last);
    print(_email);
    print(_phone);

    setState(() {
      _data = _first + "," + _last + "," + MyApp.prefs.getString("club_name").replaceAll(" ", "");
    });

    Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((spread){
      spread.refresh();
      Worksheet sheet = spread.worksheetByTitle("Sheet1");
      var new_row = [_first, _last, "Beginner", 0, "No", _email, _phone];
      sheet.values.appendRow(new_row);
    });

    // Cause collback after this next frame (ref: https://api.flutter.dev/flutter/scheduler/SchedulerBinding/addPostFrameCallback.html / https://stackoverflow.com/questions/49466556/flutter-run-method-on-widget-build-complete)
    WidgetsBinding.instance
        .addPostFrameCallback((_) => saveAndShare(context, _email));
  }

  // Saving image (ref: https://stackoverflow.com/questions/63312348/how-can-i-save-a-qrimage-in-flutter)
  void saveAndShare(BuildContext context, String email) async{
    print("In saveAndShare");
    try {
      RenderRepaintBoundary boundary = globalKey.currentContext.findRenderObject();
      var image = await boundary.toImage();
      ByteData byteData = await image.toByteData(format: ImageByteFormat.png);
      Uint8List pngBytes = byteData.buffer.asUint8List();

      // Save image locally
      final tempDir = await getApplicationDocumentsDirectory();
      print("tempDir = ${tempDir}");
      // String myDir = r"C:\Users\deziu\Documents\MembershipApp";
      final file = await new File('${tempDir.path}/image.png').create();
      // final file = await new File('${myDir}/image.png');
      file.create();
      await file.writeAsBytes(pngBytes);

      // Upload image to drive and share with club account
      return await Utils.getCreds(context).then((creds) async {
        // Find correct sheet ID
        final drive_scopes = [drive.DriveApi.DriveScope];
        return await clientViaServiceAccount(creds, drive_scopes).then((
            AuthClient client) async {
          // [client] is an authenticated HTTP client.
          var api = new drive.DriveApi(client);

          // Upload and update permissions
          var response = await api.files.create(drive.File()..name = "${_first}_${_last}.png"..parents=[folderID],
          uploadMedia: drive.Media(file.openRead(), file.lengthSync())).then((media) async{
            print("media.webViewLink = " + media.webViewLink.toString());
            print("media.id = " + media.id.toString());
            drive.Permission request = drive.Permission();
            request.type = "user";
            request.role = "writer";
            request.emailAddress = MyApp.prefs.getString("email");

            debugPrint("Before permissions");
            api.permissions.create(request, media.id);
            debugPrint("After permissions");

            await Utils.findFile(context, "", "${_first}_${_last}.png", api).then((img){
              print("img = " + img.name);
              print("img.webViewLink = " + img.webViewLink.toString());
              media.webViewLink=img.webViewLink;
            });

            // Send email with drive link to image
            final mailtoLink = Mailto(
                to: [email],
                subject: "Welcome!!",
                body: """Thanks for joining! We're happy to have you.
Here's the GoogleDrive link to your personal QRcode below (copy and paste into browswer if needed):

${media.webViewLink}

Make sure to save/screenshot the QRcode for signing in. Can't wait to see you!!
-See you next class!
Pulso Caribe at UCF

"""
            );
            print("mailtoLink = " + mailtoLink.toString());


            // Start client mail service to send email
            launch(mailtoLink.toString());
          });

        });

      });

    } catch(e) {
      print(e.toString());
    }
  }
}

class EnableButton extends StatefulWidget {
  @override
  EnableButtonState createState() => new EnableButtonState();
}

class EnableButtonState extends State<EnableButton> {

  int counter = 0;
  List<String> strings = ["Flutter", "Is", "Awesome"];
  String displayedString = "";

  //you can also declare variables like this
  // var counter = 0;
  // var strings = ["Flutter", "Is", "Awesome"];

  void onPressed(){
    setState(() {
      displayedString = strings[counter];
      counter = counter < 2 ? counter+1 : 0;
    });
  }

  @override
  Widget build(BuildContext context){
    return new Scaffold(
        appBar: new AppBar(title: new Text("Stateful Widget!"), backgroundColor: Colors.deepOrange),
        body: new Container(
            child: new Center(
                child: new Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      new Text(displayedString, style: new TextStyle(fontSize: 30.0, fontWeight: FontWeight.bold)),
                      new Padding(padding: new EdgeInsets.all(15.0)),
                      new RaisedButton(
                          child: new Text("Press me!", style: new TextStyle(color: Colors.white, fontStyle: FontStyle.italic, fontSize: 20.0)),
                          color: Colors.red,
                          onPressed: onPressed
                      )
                    ]
                )
            )
        )
    );
  }
}
