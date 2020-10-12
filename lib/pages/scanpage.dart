import 'dart:developer';

import 'package:MembershipApp/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:barcode_scan/barcode_scan.dart';
import 'package:flutter/services.dart';
import 'package:gsheets/gsheets.dart';
import 'dart:io' show Platform;
import '../bloc.navigation_bloc/navigation_bloc.dart';
import '../driveUtils.dart';
//import 'package:flutter_qr_bar_scanner/qr_bar_scanner_camera.dart';

class ScanPage extends StatefulWidget with NavigationStates {
  ScanPage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  ScanPageState createState() => ScanPageState();
}

class ScanPageState extends State<ScanPage> {

  final formKey = GlobalKey<FormState>();
  String _first, _last, _email, _phone;
  int row_;
  bool _signInEnabled=false;

  ScanResult scanResult;

  var _aspectTolerance = 0.00;
  var _numberOfCameras = 0;
  var _selectedCamera = -1;
  var _useAutoFocus = true;
  var _autoEnableFlash = false;

  TextEditingController _firstController = TextEditingController(),
      _lastController = TextEditingController(),
      _levelController = TextEditingController(),
      _numController = TextEditingController();

  static final _possibleFormats = BarcodeFormat.values.toList()
    ..removeWhere((e) => e == BarcodeFormat.unknown);

  List<BarcodeFormat> selectedFormats = [BarcodeFormat.qr];

  @override
  // ignore: type_annotate_public_apis
  initState() {
    super.initState();
    var b = RaisedButton(
      // onPressed: _confirmEnabled ? () => setState(() => _confirm()) : null,
        child: Text('Confirm'));
  }

  @override
  Widget build(BuildContext context) {

    debugPrint("row_ = " + row_.toString());
    var contentList = <Widget>[
      // if (scanResult != null)
      Card(
        child: Column(
          children: <Widget>[
            Form(
              key: formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  TextField(
                    decoration: InputDecoration(
                      labelText: 'Would you like to sign this person in?',
                      enabled: false,
                    ),
                  ),
                  TextField(
                    controller: _firstController,
                    decoration: InputDecoration(
                      labelText: 'First name:',
                      enabled: false,
                    ),
                  ),
                  TextField(
                    controller: _lastController,
                    decoration: InputDecoration(
                      labelText: 'Last name:',
                      enabled: false,
                    ),
                    // obscureText: true,
                  ),
                  TextField(
                    controller: _levelController,
                    decoration: InputDecoration(
                      labelText: 'Level:',
                      enabled: false,
                    ),
                    enableInteractiveSelection: false,
                  ),
                  TextField(
                    controller: _numController,
                    decoration: InputDecoration(
                      labelText: 'Phone number:',
                      enabled: false,
                    ),

                    // obscureText: true,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: <Widget>[
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: RaisedButton(
                          onPressed: scan,
                          child: Text("Scan"),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: RaisedButton(
                          onPressed:  _signInEnabled ? _signIn : null,
                          child: Text('Sign in'),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ];

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: Text('Barcode Scanner Example'),
          actions: <Widget>[
            // IconButton(
            //   icon: Icon(Icons.camera),
            //   tooltip: "Scan",
            //   onPressed: scan,
            // )
          ],
        ),
        body: ListView(
          scrollDirection: Axis.vertical,
          shrinkWrap: true,
          children: contentList,
        ),
      ),
    );
  }

  Future _signIn() async{

    // Sign person in
    if (_signInEnabled) {
      setState(() {
        _signInEnabled = false;
        // setBtn();
      });

      Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((spread) async {
        Worksheet sheet = spread.worksheetByTitle("Sheet1");
        final cell = await sheet.cells.cell(column: 5, row: row_);
        cell.post("Yes");
      });
    }
    // Go to scan screen
    else{

    }
  }

  Future scanned() async{
    debugPrint("scanResult = " + scanResult.rawContent);
    List<String> parsed = scanResult.rawContent.split(",");
    _first = parsed[1];
    _last = parsed[2];
    debugPrint("Testing");
    Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((spread) async{
      Worksheet sheet = spread.worksheetByTitle("Sheet1");
      print("sheet.title = " +sheet.title);

      // Find row index of entry
      sheet.values.allRows().then((rows) async{
        // Find rows that match name
        int i = 1;
        for (var row in rows){
          debugPrint("row = " + row.toString());
          if (row[0] == parsed[1] && row[1] == parsed[2]){
            debugPrint("Match.");
            if (row[4] == "No"){
              row_ = i;
              setState(() {
                _signInEnabled=true;
                _firstController.text = row[0];
                _lastController.text = row[1];
                _levelController.text = row[2];
              });
              debugPrint("i = " + i.toString());
              break;
            }
          }
          i++;
        }

        sendPopup();
      });

    });
  }
  Future scan() async {
    try {
      var options = ScanOptions(
        strings: {
          "cancel": "Cancel",
          "flash_on": "Flash on",
          "flash_off": "Flash off",
        },
        restrictFormat: selectedFormats,
        useCamera: _selectedCamera,
        autoEnableFlash: _autoEnableFlash,
        android: AndroidOptions(
          aspectTolerance: _aspectTolerance,
          useAutoFocus: _useAutoFocus,
        ),
      );


      _firstController.text = _lastController.text = _levelController.text = "";
      var result = await BarcodeScanner.scan(options: options);


      scanResult = result;

      // Post-process results
      await scanned();

    } on PlatformException catch (e) {
      var result = ScanResult(
        type: ResultType.Error,
        format: BarcodeFormat.unknown,
      );

      if (e.code == BarcodeScanner.cameraAccessDenied) {
        setState(() {
          result.rawContent = 'The user did not grant the camera permission!';
        });
      } else {
        result.rawContent = 'Unknown error: $e';
      }
      setState(() {
        scanResult = result;
      });
    }
  }

  Widget sendPopup (){
    showDialog(context: context, builder: (BuildContext context){
      return AlertDialog(
          content: Stack(
            children: <Widget>[
              Text(
                "This QR Code does not belong to any current member",
                textAlign: TextAlign.center,
              )
            ],
          )
      );
    });
  }
}
