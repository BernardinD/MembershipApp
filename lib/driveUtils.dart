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
  static String _webLink = null;

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
  static String get webLink => _webLink;

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

  // Return list of existing directories along a path, up to the point where the path exists
  static Future<List<drive.File>> findFolders(BuildContext context, List<String> names) async{
    return await Utils.getCreds(context).then((creds) async {
      // Find correct sheet ID
      final drive_scopes = [drive.DriveApi.DriveScope];
      return await clientViaServiceAccount(creds, drive_scopes).then((
          AuthClient client) async {
        // [client] is an authenticated HTTP client.
        var api = new drive.DriveApi(client);

        print("right before loop");
        List<drive.File> ret_folders = new List<drive.File>();
        for(int i = 0; i < names.length; i++) {
          print("inside loop");
          print("ret_folders[i - 1] = " + ((i - 1 >= 0) ? ret_folders[i - 1].toString(): ""));
          // Run query
          // Return null if (we are passed the root) && (there exists no folder above)
          drive.File sub_ = (i - 1 >= 0) && (ret_folders[i - 1]== null) ? null : await api.files.list(
            // Set parentID if idx is passed root
            q: """${mimetypes["folder"]}
                  ${(i - 1 >= 0) ? "and '${ret_folders[i - 1].id}' in parents" : ""}
                  and name = '${names[i]}'
                  """,
            spaces: 'drive').then((folders) {
              drive.File sub_ = folders.files.length > 0
                  ? folders.files[0]
                  : null;
              return sub_;
          }, onError: (e) => print("Create: " + e.toString()));

          print("sub_ = " + sub_.toString());
          ret_folders.add(sub_);
        }
        print("after loop");
        for(drive.File folder in ret_folders){
          print("folder: " +folder.toString());
        }
        return ret_folders;
      });
    });
  }

  static Future createSheet(String title)async{
    Spreadsheet sh = await _SheetApi.createSpreadsheet(title);
    await sh.share(MyApp.prefs.getString('email'), type:PermType.user, role:PermRole.owner).catchError((e){
      print("---share got an error---");
      print(e);
    });
    var sheet = sh.worksheetByTitle("Sheet1");
    await sheet.values.appendRow(["First Name", "Last Name", 'Level', "Attendences", "Signed-in", "Email", "Phone #"]);

    // Clear spreadsheet
    clearSpread();

  }

  // Creates a folder in the drive of the set email in settings
  // Becomes a sub-folder if a parent is given
  static Future<drive.File> createFolders(BuildContext context, String name, String parentID) async{
    return await Utils.getCreds(context).then((creds) async {
      // Find correct sheet ID
      final drive_scopes = [drive.DriveApi.DriveScope];
      return await clientViaServiceAccount(creds, drive_scopes).then((
          AuthClient client) async {
        // [client] is an authenticated HTTP client.
        var api = new drive.DriveApi(client);

        print("new folder name = " + name);
        return await api.files.create(
            drive.File()..name=name..mimeType='application/vnd.google-apps.folder'..parents=[parentID],).catchError((e){
              print("Caught create error");
              print(e);
        }).then((file) async {

          print("new file: "+ file.name);
          print("parentID = " + parentID);

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

  static void clearSpread(){
    _Spread = null;
    print("Spreadsheet cleared");
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
          var api = new drive.DriveApi(client);

          final gsheetsApi = await Utils.getSheetApi(context);

          // print("mimtypes = " + mimetypes.keys.toString());
          _Spread = await Utils.findFile(
              context, mimetypes['spreadsheet'], name, api)
              .then((file) async {
            if (file != null) {
              debugPrint("file = " + file.name);
              print("file.webViewLink = " + file.webViewLink.toString());
              _webLink = file.webViewLink;
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