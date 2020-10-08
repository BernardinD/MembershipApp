import 'dart:io';

import 'package:MembershipApp/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc.navigation_bloc/navigation_bloc.dart';

class HomePage extends StatelessWidget with NavigationStates {
  @override
  Widget build(BuildContext context) {
    // MyApp.prefs.clear();
    return Scaffold(
        appBar: AppBar(
          title:
            Center(
               child: Text(
                  "HomePage",
                  style: TextStyle(fontWeight: FontWeight.w900, fontSize: 28),
                ),
            ),
        ),
        body: SingleChildScrollView(
        child: Center(
          child: Column(
              children: <Widget>[
                Padding(
                  padding: const EdgeInsets.only(top: 22, bottom: 8),
                  child:  Image(
                    image: AssetImage('C:/Users/deziu/Downloads/iphone-388387_1920.jpg'),
                    width: 500,
                    height: 500,
                  ),
                ),
              ]
          ),
        ),
      ),
    );
  }
}
