import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:googleapis/cloudbuild/v1.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:googleapis/drive/v2.dart' as drive;
import 'package:googleapis_auth/auth_io.dart';
import 'package:gsheets/gsheets.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class Utils{

  static GSheets _SheetApi = null;
  static drive.File _Sheet = null;
  static ServiceAccountCredentials _Creds = null;

  // Mimetypes (ref: https://developers.google.com/drive/api/v2/mime-types)
  static final Map _mimetypes =  const {
    'pdf' : "application/pdf",
    'text' : "text/plain",
    'docs' : "application/vnd.google-apps.document",
    'spreadsheet' : "application/vnd.google-apps.spreadsheet",
    'slides' : "application/vnd.google-apps.presentation",
    'all' : null,
  };
  static Map get mimetypes => _mimetypes;

  static Future<ServiceAccountCredentials> getCreds(BuildContext context) async{
    if (_Creds != null) {
      print("Came here");
      return _Creds;
    }
    else{
      print("Before:");
      var jsonCredentials = await loadAsset(context);
      print("Credentials = " + jsonCredentials.runtimeType.toString());
      Map<String, dynamic> user = json.decode(jsonCredentials);

      print("jsonEncode(user) = " + jsonEncode(user));
      _Creds = new ServiceAccountCredentials.fromJson(user);
      print("-----GOT CREDENTIALS----");
      return _Creds;
    }
  }

  static Future<String> loadAsset(BuildContext context) async{
    return await DefaultAssetBundle.of(context).loadString("./client_secret.json");
  }

  static Future<GSheets> getSheetApi(BuildContext context) async{
    if (_SheetApi != null) return _SheetApi;
    else{
      String jsonCredentials = await loadAsset(context);
      print("Credentials = " + jsonCredentials);
      _SheetApi = GSheets(jsonCredentials);
      return _SheetApi;
    }
  }

  static Future<Spreadsheet> getSpread(BuildContext context, String name) async {
    // Google credentials
    return await Utils.getCreds(context).then((creds) async {
      // Find correct sheet ID
      final drive_scopes = [drive.DriveApi.DriveScope];
      return await clientViaServiceAccount(creds, drive_scopes).then((
          AuthClient client) async {
        // [client] is an authenticated HTTP client.
        // ...
        var api = new drive.DriveApi(client);

        final gsheetsApi = await Utils.getSheetApi(context);

        // print("mimtypes = " + mimetypes.keys.toString());
        return Utils.findFile(
            context, mimetypes['spreadsheet'], name, api)
            .then((file) async {
          print("file = " + file.title);
          return await gsheetsApi.spreadsheet(file.id).then((sheet) {
            return sheet;
          });
        });
        client.close();
      }, onError: (e) => print("FilesError: " + e.toString()));
    }, onError: (e) => print("DriveError: " + e.toString()));
  }

  static Future<drive.File> findFile(BuildContext context, String mimeType, String name, drive.DriveApi api) async{
    if (_Sheet != null){
      print("Came here");
      return _Sheet;
    }
    else {
      return api.files.list(
          q: "mimeType='$mimeType'",
          spaces: 'drive').then((value) {
        debugPrint("values = " + value.items.toString());
        int i = 0;
        for (var item in value.items) {
          if (name == item.title) {
            return item;
          }
        }
      }, onError: (e) => print("list: " + e.toString()));
    }
  }
}