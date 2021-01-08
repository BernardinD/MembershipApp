import 'package:flutter/material.dart';
import 'package:progress_dialog/progress_dialog.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'sidebar/sidebar_layout.dart';
import 'package:MembershipApp/driveUtils.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {

  static SharedPreferences _prefs;
  static SharedPreferences get prefs => _prefs;
  static Color _primaryColor = Color(0xFF262AAA);
  static Color get primaryColor => _primaryColor;
  static ProgressDialog _pr;
  static ProgressDialog get pr => _pr;

  Future initSettings(BuildContext context)async{
    if (_prefs == null)
      _prefs = await SharedPreferences.getInstance().catchError((onError){
        debugPrint("Main: ${onError}");
      });

    if (_pr == null){
      _pr = new ProgressDialog(context, isDismissible: false);
      _pr.style(
          message: 'Please Waiting...',
          borderRadius: 10.0,
          backgroundColor: Colors.white,
          progressWidget: CircularProgressIndicator(),
          elevation: 10.0,
          insetAnimCurve: Curves.easeInOut,
          progress: 0.0,
          maxProgress: 100.0,
          progressTextStyle: TextStyle(
              color: Colors.black, fontSize: 13.0, fontWeight: FontWeight.w400),
          messageTextStyle: TextStyle(
              color: Colors.black, fontSize: 19.0, fontWeight: FontWeight.w600)
      );
    }

    // Initial initialization of Spreadsheet
    await driveUtils.loadAsset(context).then((value) async{
      return await driveUtils.getSpread(context, MyApp.prefs.getString("sheet")).then((ret){
        return ret.toString();
      }, onError: (e){
        throw ("Spreadsheet could not be found");
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
          scaffoldBackgroundColor: Colors.white,
          primaryColor: Colors.white
      ),
      home: Builder(builder: (context) {
        initSettings(context);
        return SideBarLayout();
      }),
    );
  }
}
