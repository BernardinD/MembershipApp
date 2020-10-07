import 'dart:io';

import 'package:MembershipApp/main.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:MembershipApp/driveUtils.dart';
import '../bloc.navigation_bloc/navigation_bloc.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:googleapis/drive/v2.dart' as drive;
import 'package:googleapis_auth/auth_io.dart';
import 'package:gsheets/gsheets.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class DrivePage extends StatefulWidget with NavigationStates {
  @override
  DrivePageState createState() => new DrivePageState();
}

class DrivePageState extends State<DrivePage>  {
  final formKey = GlobalKey<FormState>();
  String _first, _last, _email, _phone, _data ="";
  bool _confirmEnabled = false, _submitEnabled = true;

  // Use this controller to clear all text fields
  TextEditingController _controller = TextEditingController();

  Future<String> loadAsset() async{
    String ret;
    return await DefaultAssetBundle.of(context).loadString("./client_secret.json").then((value) {
      print("----- HERE ------");
    }, onError: (e) => print("Inside LoadAsset: " + e));
  }
  @override
  void initState() {
    super.initState();

    // Initialize everything
    Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((spread) {
      print("Final result: " + spread.toString());
    });

  }
  @override
  Widget build(BuildContext context) {
    _controller.text = 'Testing123@';
    return Center(
      child: Column(
          children: <Widget>[
            Text(
              "Google Drive Page",
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
                      QrImage(
                        data: _data,
                        version: QrVersions.auto,
                        size: 220,
                        gapless: false,
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
                        controller: _controller,
                        decoration: InputDecoration(
                            labelText: 'First name:'
                        ),
                        validator: (input) => input.length < 2 ? 'You need at least 8 characters' : null,
                        onSaved: (input) => _first = input,
                      ),
                      TextFormField(
                        controller: _controller,
                        decoration: InputDecoration(
                            labelText: 'Last name:'
                        ),
                        validator: (input) => input.length < 2 ? 'You need at least 8 characters' : null,
                        onSaved: (input) => _last = input,
                        // obscureText: true,
                      ),
                      TextFormField(
                        controller: _controller,
                        decoration: InputDecoration(
                            labelText: 'Email:'
                        ),
                        validator: (input) => !input.contains('@') ? 'Not a valid Email' : null,
                        onSaved: (input) => _email = input,
                      ),
                      TextFormField(
                        controller: _controller,
                        decoration: InputDecoration(
                            labelText: 'Phone number:'
                        ),
                        validator: (input) => input.length < 10 ? 'You need at least 8 characters' : null,
                        onSaved: (input) => _phone = input,
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
                              onPressed: _confirmEnabled ? () => setState(() => _submit()) : null,
                              child: Text('Confirm'),
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
      formKey.currentState.save();
      print(_first);
      print(_last);
      print(_email);
      print(_phone);

      _data = _first + "," + _last + "," + "PulsoCaribe";
      Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((spread){
        Worksheet sheet = spread.worksheetByTitle("Sheet1");
        var new_row = [_first, _last, "Beginner", 0, "No", _email, _phone];
        sheet.values.appendRow(new_row);
      });
    }
  }
}