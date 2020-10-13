import 'dart:io';

import 'package:MembershipApp/main.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:googleapis/cloudbuild/v1.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:googleapis/drive/v3.dart' as drive;
import 'package:googleapis_auth/auth_io.dart';
import 'package:gsheets/gsheets.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class Utils{

  static GSheets _SheetApi = null;
  static Spreadsheet _Spread = null;
  static ServiceAccountCredentials _Creds = null;

  // Mimetypes (ref: https://developers.google.com/drive/api/v2/mime-types)
  static final Map _mimetypes =  const {
    'pdf' : "mimeType = 'application/pdf'",
    'text' : "mimeType = 'text/plain'",
    'docs' : "mimeType = 'application/vnd.google-apps.document'",
    'spreadsheet' : "mimeType = 'application/vnd.google-apps.spreadsheet'",
    'slides' : "mimeType = 'application/vnd.google-apps.presentation'",
    'folder' : "mimeType = 'application/vnd.google-apps.folder'",
    'image/png' : "mimeType = 'application/vnd.google-apps.photo'",
    'all' : null,
  };
  static Map get mimetypes => _mimetypes;

  static Future<ServiceAccountCredentials> getCreds(BuildContext context) async{
    if (_Creds != null) {
      return _Creds;
    }
    else{
      var jsonCredentials = await loadAsset(context);

      try {
        Map<String, dynamic> user = json.decode(jsonCredentials);
        // print("jsonEncode(user) = " + jsonEncode(user));
        _Creds = new ServiceAccountCredentials.fromJson(user);
      }
      catch (e){
        debugPrint("getCreds: " + e.toString());
      }
      return _Creds;
    }
  }

  static Future<List<drive.File>> findFolders(BuildContext context, String parent, String sub) async{
    return await Utils.getCreds(context).then((creds) async {
      // Find correct sheet ID
      final drive_scopes = [drive.DriveApi.DriveScope];
      return await clientViaServiceAccount(creds, drive_scopes).then((
          AuthClient client) async {
        // [client] is an authenticated HTTP client.
        var api = new drive.DriveApi(client);

        return api.files.list(
            q: "${mimetypes["folder"]} and name = '${parent}'",
            spaces: 'drive').then((folders){
              drive.File parent_ = folders.files.length > 0 ? folders.files[0] : null;
              if (sub != null){
                return api.files.list(
                    q: """${mimetypes["folder"]} and 
                    name = '${sub}' and '${parent_.id}' in parents""",
                    spaces: 'drive').then((folders) {
                      drive.File sub_ = folders.files.length > 0 ? folders.files[0] : null;
                      return [parent_, sub_];
                }, onError: (e) => print("Create: " + e.toString()));
              }
              return [parent_, null];
            });
      });
    });
  }

  static Future<drive.File> createFolders(BuildContext context, String name, String parentID) async{
    return await Utils.getCreds(context).then((creds) async {
      // Find correct sheet ID
      final drive_scopes = [drive.DriveApi.DriveScope];
      return await clientViaServiceAccount(creds, drive_scopes).then((
          AuthClient client) async {
        // [client] is an authenticated HTTP client.
        var api = new drive.DriveApi(client);

        return await api.files.create(
            drive.File()..name=name..mimeType=mimetypes["folder"]..parents=[parentID]).then((file) async {

              // Change Ownership
              await api.permissions.create(drive.Permission()..type='user'..role='Owner'..emailAddress=MyApp.prefs.getString("email"), file.id, transferOwnership: true);

              return file;
            });

      });
    });
  }

  static Future<String> loadAsset(BuildContext context) async{
    return await File("./client_secret.json").readAsString().catchError((e) {return File(MyApp.prefs.getString("secret")).readAsString();});
  }

  static Future<GSheets> getSheetApi(BuildContext context) async{
    if (_SheetApi != null) return _SheetApi;
    else{
      String jsonCredentials = await loadAsset(context);
      _SheetApi = GSheets(jsonCredentials);
      return _SheetApi;
    }
  }

  static Future<Spreadsheet> getSpread(BuildContext context, String name) async {

    if (_Spread != null){
      return _Spread;
    }
    else {
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
          _Spread = await Utils.findFile(
              context, mimetypes['spreadsheet'], name, api)
              .then((file) async {
            if (file != null) {
              debugPrint("file = " + file.name);
              print("file.webViewLink = " + file.webViewLink.toString());
              return await gsheetsApi.spreadsheet(file.id).then((sheet) {
                return sheet;
              });
            }
            else {
              throw ("Spreadsheet does not exists.");
            }
          });
          client.close();
          return _Spread;
        }, onError: (e) => print("FilesError: " + e.toString()));
      }, onError: (e) => print("DriveError: " + e.toString()));
    }
  }

  static Future<drive.File> findFile(BuildContext context, String mimeType, String name, drive.DriveApi api) async{
    print("len = " + "".length.toString());
    String mimetype = mimeType.length>0 ? "${mimeType} and " : "";
    print("mimetype = " + mimetype);
    return api.files.list(
        q: "${mimetype} name = '${name}'",
        spaces: 'drive', $fields: "files(modifiedTime,id,name,createdTime,version,size,md5Checksum,webViewLink)").then((value) {
      debugPrint("values = " + value.files.toString());
      return value.files[0];
    }, onError: (e) => print("list: " + e.toString()));
  }
}