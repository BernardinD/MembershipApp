import 'dart:async';
import 'dart:developer';
import 'dart:io';

import 'package:MembershipApp/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:MembershipApp/bloc.navigation_bloc/navigation_bloc.dart';
import 'package:googleapis_auth/auth.dart';
import 'package:rxdart/rxdart.dart';

// import '../bloc.navigation_bloc/navigation_bloc.dart';
import 'package:MembershipApp/sidebar/menu_item.dart';
import 'package:MembershipApp/driveUtils.dart';

class SideBar extends StatefulWidget {

  _SideBarState SidebarState = _SideBarState();
  @override
  _SideBarState createState() => SidebarState;
  
  void onIconPressed(){
	  SidebarState.onIconPressed();
  }

  AnimationController getAnimationController(){
    debugPrint("SidebarState._animationController = " + (SidebarState._animationController == null).toString() );
    return SidebarState._animationController;
  }
}

class _SideBarState extends State<SideBar> with SingleTickerProviderStateMixin<SideBar> {
  AnimationController _animationController;
  StreamController<bool> isSidebarOpenedStreamController;
  Stream<bool> isSidebarOpenedStream;
  StreamSink<bool> isSidebarOpenedSink;
  final _animationDuration = const Duration(milliseconds: 500);

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(vsync: this, duration: _animationDuration);
    isSidebarOpenedStreamController = PublishSubject<bool>();
    isSidebarOpenedStream = isSidebarOpenedStreamController.stream;
    isSidebarOpenedSink = isSidebarOpenedStreamController.sink;
  }

  @override
  void dispose() {
    _animationController.dispose();
    isSidebarOpenedStreamController.close();
    isSidebarOpenedSink.close();
    super.dispose();
  }

  void onIconPressed() {
    final animationStatus = _animationController.status;
    final isAnimationCompleted = animationStatus == AnimationStatus.completed;

    if (isAnimationCompleted) {
      isSidebarOpenedSink.add(false);
      _animationController.reverse();
    } else {
      isSidebarOpenedSink.add(true);
      _animationController.forward();
    }
  }

  void changePage(BuildContext context, NavigationEvents e,) async{
    // Make sure credentials and spreadsheet
    if(e != NavigationEvents.HomePageClickedEvent && e != NavigationEvents.SettingsPageClickedEvent){
      // Check json first, then sheet; If either fails block change and show popup
      var response = await Utils.loadAsset(context).then((value) async{
        return await Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((ret){
          return ret.toString();
        }, onError: (e){
          throw ("Spreadsheet could not be found");
        });
      }).catchError( (e){
        showDialog(context: context, builder: (BuildContext context){
          return AlertDialog(
              content: Stack(
                children: <Widget>[
                  Text(
                    e.toString() + "\n\n Please double check settings",
                    textAlign: TextAlign.center,
                  )
                ],
              )
          );
        });
        onIconPressed();
        throw(e);
      });
    }
    BlocProvider.of<NavigationBloc>(context).add(e);
    onIconPressed();
  }

  Future reloadSpread(BuildContext context) async{
    // Check json first, then sheet; If either fails block change and show popup
    await Utils.loadAsset(context).then((value) async{
      return await Utils.getSpread(context, MyApp.prefs.getString("sheet")).then((sheet) async{
        await sheet.refresh();
        showDialog(context: context, builder: (BuildContext context){
          return AlertDialog(
              content: Stack(
                children: <Widget>[
                  Text(
                    "Spreadsheet has been reloaded",
                    textAlign: TextAlign.center,
                  )
                ],
              )
          );
        });
        onIconPressed();
      }, onError: (e){
        throw ("Spreadsheet could not be found");
      });
    }).catchError( (e){
      showDialog(context: context, builder: (BuildContext context){
        onIconPressed();
        return AlertDialog(
            content: Stack(
              children: <Widget>[
                Text(
                  e.toString() + "\n\n Please double check settings and wifi",
                  textAlign: TextAlign.center,
                )
              ],
            )
        );
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return StreamBuilder<bool>(
      initialData: false,
      stream: isSidebarOpenedStream,
      builder: (context, isSideBarOpenedAsync) {
        return AnimatedPositioned(
          duration: _animationDuration,
          top: 0,
          bottom: 0,
          left: isSideBarOpenedAsync.data ? 0 : -screenWidth,
          right: isSideBarOpenedAsync.data ? 0 : screenWidth - 45,
          child: Row(
            children: <Widget>[
              Expanded(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  color: const Color(0xFF262AAA),
                  height: screenHeight,
                  child: SingleChildScrollView(
                    child: Column(
                      children: <Widget>[
                        Container(
                          width: screenHeight >= screenWidth*0.6 ? screenWidth*0.8 : screenWidth*0.4,
                          child: Padding(
                            padding: const EdgeInsets.only(top: 22, bottom: 8),
                            child: Image(
                              image: AssetImage('C:/Users/deziu/Downloads/iphone-388387_1920.jpg'),
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        Divider(
                          height: 64,
                          thickness: 0.5,
                          color: Colors.white.withOpacity(0.3),
                          indent: 32,
                          endIndent: 32,
                        ),
                        Container(
                          // The Gesture doesn't apply to whole row with the Decoration for some reason
                            decoration: BoxDecoration(
                              color: Colors.amber,
                            ),
                            child: MenuItem(
                                icon: Icons.refresh_rounded,
                                title: "Reload Spreadsheet",
                                onTap: () {
                                  reloadSpread(context);
                                },
                          height: screenHeight,
                            )
                        ),
                        Divider(
                          height: 64,
                          thickness: 0.5,
                          color: Colors.white.withOpacity(0.3),
                          indent: 32,
                          endIndent: 32,
                        ),
                        MenuItem(
                          icon: Icons.home,
                          title: "Home",
                          onTap: () {
                            changePage(context, NavigationEvents.HomePageClickedEvent);
                          },
                          height: screenHeight,
                        ),
                        MenuItem(
                          icon: Icons.add_box_outlined,
                          title: "Add Members",
                          onTap: () {
                            changePage(context, NavigationEvents.AddMembersClickedEvent);
                          },
                          height: screenHeight,
                        ),
                        MenuItem(
                          icon: Icons.qr_code_scanner_rounded,
                          title: "Scan In",
                          onTap: () {
                            changePage(context, NavigationEvents.ScanPageClickedEvent);
                          },
                          height: screenHeight,
                        ),
                        // MenuItem(
                        //   icon: Icons.qr_code_scanner,
                        //   title: "Test scanner",
                        //   onTap: () {
                        //     onIconPressed();
                        //     changePage(context, NavigationEvents.TestScanPageClickedEvent);
                        //   },
                        // ),
                        Divider(
                          height: 64,
                          thickness: 0.5,
                          color: Colors.white.withOpacity(0.3),
                          indent: 32,
                          endIndent: 32,
                        ),
                        MenuItem(
                          icon: Icons.settings,
                          title: "Settings",
                          height: screenHeight,
                          onTap: () {
                            changePage(context, NavigationEvents.SettingsPageClickedEvent);
                          },
                        ),
                        MenuItem(
                          icon: Icons.exit_to_app,
                          title: "Exit",
                          height: screenHeight,
                          onTap: () {SystemChannels.platform.invokeMethod('SystemNavigator.pop');},
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              Align(
                alignment: Alignment(0, -0.9),
                child: GestureDetector(
                  onTap: () {
                    onIconPressed();
                  },
                  child: ClipPath(
                    clipper: CustomMenuClipper(),
                    child: Container(
                      width: 35,
                      height: 110,
                      color: Color(0xFF262AAA),
                      alignment: Alignment.centerLeft,
                      child: AnimatedIcon(
                        progress: _animationController.view,
                        icon: AnimatedIcons.menu_close,
                        color: Color(0xFF1BB5FD),
                        size: 25,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class CustomMenuClipper extends CustomClipper<Path> {
  @override
  Path getClip(Size size) {
    Paint paint = Paint();
    paint.color = Colors.white;

    final width = size.width;
    final height = size.height;

    Path path = Path();
    path.moveTo(0, 0);
    path.quadraticBezierTo(0, 8, 10, 16);
    path.quadraticBezierTo(width - 1, height / 2 - 20, width, height / 2);
    path.quadraticBezierTo(width + 1, height / 2 + 20, 10, height - 16);
    path.quadraticBezierTo(0, height - 8, 0, height);
    path.close();
    return path;
  }

  @override
  bool shouldReclip(CustomClipper<Path> oldClipper) {
    return true;
  }
}
