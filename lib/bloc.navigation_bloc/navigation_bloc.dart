import 'package:MembershipApp/pages/settings.dart';
import 'package:bloc/bloc.dart';
import 'package:MembershipApp/pages/add_memberpage.dart';
import 'package:MembershipApp/pages/drivepage.dart';
import 'package:MembershipApp/pages/scanpage.dart';
import 'package:MembershipApp/driveUtils.dart';
import '../pages/myaccountspage.dart';
import '../pages/myorderspage.dart';

import '../pages/homepage.dart';

enum NavigationEvents {
  HomePageClickedEvent,
  AddMembersClickedEvent,
  DriveClickedEvent,
  ScanPageClickedEvent,
  SettingsPageClickedEvent,
}

abstract class NavigationStates {}

class NavigationBloc extends Bloc<NavigationEvents, NavigationStates> {
  @override
  NavigationStates get initialState => HomePage();

  @override
  Stream<NavigationStates> mapEventToState(NavigationEvents event) async* {
    switch (event) {
      case NavigationEvents.HomePageClickedEvent:
        yield HomePage();
        break;
      case NavigationEvents.AddMembersClickedEvent:
        yield AddMemberPage();
        break;
      case NavigationEvents.DriveClickedEvent:
        yield DrivePage();
        break;
      case NavigationEvents.ScanPageClickedEvent:
        yield ScanPage();
        //yield ScanScreen();
        break;
      case NavigationEvents.SettingsPageClickedEvent:
        yield SettingsPage();
        //yield ScanScreen();
        break;
    }
  }
}
