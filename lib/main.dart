import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'sidebar/sidebar_layout.dart';
import 'package:MembershipApp/driveUtils.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {

  static SharedPreferences _prefs;
  static SharedPreferences get prefs => _prefs;

  void initSettings(BuildContext context)async{
    _prefs = await SharedPreferences.getInstance().catchError((onError){
      debugPrint("Main: ${onError}");
    });

    // Initial initialization of Spreadsheet
    await Utils.loadAsset(context).then((value) async{
      return await Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((ret){
        return ret.toString();
      }, onError: (e){
        throw ("Spreadsheet could not be found");
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    initSettings(context);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
          scaffoldBackgroundColor: Colors.white,
          primaryColor: Colors.white
      ),
      home: SideBarLayout(),
    );
  }
}
