import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gsheets/gsheets.dart';
import '../bloc.navigation_bloc/navigation_bloc.dart';
import 'package:qr_flutter/qr_flutter.dart';

import '../utils.dart';

class AddMemberPage extends StatefulWidget with NavigationStates {
  @override
  AddMemberPageState createState() => new AddMemberPageState();
}

class AddMemberPageState extends State<AddMemberPage>  {
  final formKey = GlobalKey<FormState>();
  String _first, _last, _email, _phone, _data ="";
  bool _confirmEnabled = false, _submitEnabled = true;

  // Use this controller to clear all text fields
  TextEditingController _controller = TextEditingController();

  @override
  void initState() {
    super.initState();

    // Initialize everything
    Utils.getSpread(context, "Testing").then((spread) {
      print("Final result: " + spread.toString());
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
                        decoration: InputDecoration(
                            labelText: 'First name:'
                        ),
                        validator: (input) => input.length < 2 ? 'You need at least 8 characters' : null,
                        onSaved: (input) => _first = input,
                      ),
                      TextFormField(
                        decoration: InputDecoration(
                            labelText: 'Last name:'
                        ),
                        validator: (input) => input.length < 2 ? 'You need at least 8 characters' : null,
                        onSaved: (input) => _last = input,
                        // obscureText: true,
                      ),
                      TextFormField(
                        decoration: InputDecoration(
                            labelText: 'Email:'
                        ),
                        validator: (input) => !input.contains('@') ? 'Not a valid Email' : null,
                        onSaved: (input) => _email = input,
                      ),
                      TextFormField(
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
                              onPressed: _confirmEnabled ? () => setState(() => _confirm()) : null,
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

    _data = _first + "," + _last + "," + "PulsoCaribe";;
    Utils.getSpread(context, "Testing").then((spread){
      Worksheet sheet = spread.worksheetByTitle("Sheet1");
      var new_row = [_first, _last, "Beginner", 0, "No", _email, _phone];
      sheet.values.appendRow(new_row);
    });
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
