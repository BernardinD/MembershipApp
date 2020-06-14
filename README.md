# MembershipApp

This is an app meant to help with making keeping track of members in a club.

It essentially adds on top of the usual Excel spreadsheet method by adding on a QR code that makes the search through the spreadsheet much faster and reduces the turnover time for sign-ins or membership verification

This app was created using Kivy in order to make it compatible with any OS, giving the option to add on if desired. 
This also makes it easy for converting/exporting to a mobile app version

All one would need in order to use this app is a GoogleSheets spreadsheet of there members and a google client key

## Installations
* Install Python3: https://www.python.org/downloads/ (Search for version 3.6.7)
	* After launching the installation file make sure to click the check box at the bottom of the popup window that states adding Python to PATH
* Run `pip install -r requirements` from the folder where you copied this repository
### Windows:
If getting an error involving sld2 run:
```
python -m pip install kivy.deps.sdl2 kivy.deps.glew
```



## Use

On first creation the app will need to be built using the command `pyinstaller --onefile .\Membership.spec`
after adding a 'client_secret.json' file to the assets directory as well as an 'club_logo.ico' file to the head directory

## Working on
* ~~Adding a functional settings page for dynamic customization~~
* Adding a free way to send each member their QR code over SMS through Kivy or some other cross-plaform compatible desktop library
* ~~Make FileBrowser class in libs/classes/browse.py a singleton-class so that binding browser_btn can be completly internal~~

---------
* ~~Have all logos in app dynamically read from json entry~~
* ~~Change the QRCode generation to be unique to arbitrary club~~
* ~~Finish commenting instructions for all parts and functionalities of app~~
* ~~Alter the logo selection so that only jpg/jpeg and png selections are allowed~~
* ~~Make sheet creation dynamic (i.e. include primary contact field)~~

