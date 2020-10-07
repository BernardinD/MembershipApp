import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'sidebar/sidebar_layout.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {

  static SharedPreferences _prefs;
  static SharedPreferences get prefs => _prefs;

  void initSettings()async{
    _prefs = await SharedPreferences.getInstance().catchError((onError){
      debugPrint("Main: ${onError}");
    });
  }

  @override
  Widget build(BuildContext context) {
    initSettings();
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
