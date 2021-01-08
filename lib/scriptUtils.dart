import 'package:MembershipApp/main.dart';
import 'package:flutter/cupertino.dart';
import 'package:googleapis/drive/v3.dart' as drive;
import 'package:googleapis_auth/auth_io.dart';
import 'package:gsheets/gsheets.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:MembershipApp/driveUtils.dart';

class scriptUtils{

  static const String FORM_CREATE_URL = "https://script.google.com/macros/s/AKfycbz5glsTfPdxeAh3Gjyay72QF_UvDs514BA7VS9XtLfnMI5CKE3soeFeFA/exec";

  // Function to invoke Google Apps Script at FORM_CREATE_URL that creates form
  // Returns result of running URL with url_launcher
  static createForm(BuildContext context, String formName) async{
    // Get current spreadsheet
    Spreadsheet sheet = await driveUtils.getSpread(context, MyApp.prefs.getString('sheet'));
    // If spreadsheet exists, send its ID to form creation script
    if (sheet is Spreadsheet) {
      // Returns result of running URL
      return launch("${FORM_CREATE_URL}?ID=${sheet.id}?formName=${formName}?email=${MyApp
          .prefs.getString("email")}");
    }
  }
}