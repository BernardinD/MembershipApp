import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc.navigation_bloc/navigation_bloc.dart';

class HomePage extends StatelessWidget with NavigationStates {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
          children: <Widget>[
            Text(
              "HomePage",
              style: TextStyle(fontWeight: FontWeight.w900, fontSize: 28),
            ),
            FlatButton(
              onPressed: (){
                BlocProvider.of<NavigationBloc>(context).add(NavigationEvents.SettingsPageClickedEvent);
              },
              child: Text(
                  "Change screen"
              ),
            )
          ]
      ),
    );
  }
}
