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
### Needed:
* Google credentials file 'client_secret.json'
* '.ico' file of club logo (optional - if you want to customize the image of the application)

### Creating 'client_secret.json' file:

#### Activate option to connect:
* Go to this page: https://console.developers.google.com/project
* Select the option to "Create Project", give it a name and create it
* On the side-left menu go to “APIs & Services > Library”
* Search for and enable both "Drive API" and "Sheets API" respectively
#### Create linking file:
* On the side-left menu go to “APIs & Services > Credentials”
* Choose the option to "Create Credentials” and select "Service Account"
* Give this a name and create it (press continue until it is created)
* Click on the item you've just created (towards the bottom of the page) and at the bottom of the next page select "Add key > Create new key" 
* Select 'JSON' and create the file. 
* Save this file with the name 'client_secret'

## Build app

### Windows
On first creation the app will need to be built using the command `pyinstaller --onefile .\Membership.spec`
after adding a 'client_secret.json' file to the assets directory as well as an 'club_logo.ico' file to the head directory if you wish the app to have your club logo

After the command finishes you'll find the application in the 'dist' folder

### Android
`pip3 install --upgrade Cython`
On a Linux machine you will have to run `buildozer -v android debug deploy run logcat`

To do a fresh build run `buildozer -v android clean` first

## Working on
* Adding a free way to send each member their QR code over SMS through Kivy or some other cross-plaform compatible desktop library
* Include Mac and Linux installation instructions
