# Scantron ![CI](https://github.com/Edenworks/Scantron/workflows/CI/badge.svg)

An Android app that displays raft information queried from Business Central using RFID tag scans from a TSL 1166 handheld device.

## Installing the Application 

This application runs on Android devices (Android 9.0 Pie - API Level 28) or greater. As a private application, it is not hosted on 
the Google Play store. Instead it must be "side-loaded" (a fancy way of saying it must be loaded from your own sources). This means 
that you're going to get some warnings along the way that this application wasn't developed by a signed source. Don't Panic. It's 
all good.

  - Enter Developer Mode (First Time Only)
    - Enter `Configuration Options` (the gear in the top pulldown menu or however you'd like to reach `Settings`)
    - Scroll down and select `About`
    - Scroll down and tap `Build Number` ten times! You'll see popups cheering you on until officially in developer mode.
  - Download the Latest Version
    - Open your favorite web browser (likely Chrome on Android)
    - Go to `github.com` & sign in with your account
    - Select `releases` and click on the latest release to download
    - Twiddle your fingers or study kung-fu while you wait
    - Click `open` on the popup once the file is downloaded
    - Click `open anyway` and so-on when warned about unsigned applications
  - Run It! 

## Usage

This application has a few modes of operation. By default, it will start in `Scan Raft Info` mode. To select a mode, 
click the `Upward Farms` logo in the upper left corner of the application to present the mode list. Selecting one 
of these will immediately switch to that mode.

Below this is a listing of all RFID scanners detected and their current connection status. The application will 
attempt to connect to the most recent RFID scanner on launch. The user may toggle connect/disconnect status with 
any of the detected RFID scanners by clicking that scanner on this list. To refresh to list of scanners (by rescanning 
for them), drag down on this part of the screen until the progress spinner is shown.

### Scan Raft Info

In this mode, the RFID scanner is used to collect information about rafts. Any scanned RFID is checked against the server 
and the current status is returned. The returned information can be clicked for additional detailed information. This mode 
will continue to accumulate rafts as you scan. Individual rafts can be removed by clicking the `X` icon on that raft. All
rafts can be cleared by clicking the `X` on the prompt at the bottom of the screen. 

### Manual Raft Info

This mode has all the features of `Scan Raft Info` mode, with the addition of a manual lookup prompt at the bottom of 
the screen. A raft ID can be manually entered using the popup keyboard. Information can be queried for that Raft by 
clicking the `Lookup` button. Note: This mode is only available if enabled in `Settings`.

### Inventory

`Inventory` mode is similar to `Scan Raft Info` mode, except that it's not concerned about what is being scanned. No
detail queries are made to the server. Instead, it accumulates a list of scanned RFID's and displays them in alphanumeric 
order, without additional information.

### Scan Job Refls

This mode is used as part of the correction workflow. It starts by requesting a list of outstanding correction jobs from 
the server. If there are any, these are listed for the user, allowing one to be selected. Once selected, the application 
allows scanning of rafts identically to the `Scan Raft Info` mode. Progress is presented at the bottom of the screen, so 
the user knows how many rafts have been scanned and how many should be scanned. Once the proper number of rafts have been 
scanned, an option to `Approve Scanned Rafts` is presented. If the user selects this, the list of Rafts just scanned 
will be submitted as the corrected collection for the requested job.

### Settings

The last mode is a settings screen. It presents a number of options which can be used to customize the use of Scantron. 
It is recommended that only users who understand these settings make changes here, as the repurcussions are likely to 
include stopping the application from speaking to the server or the RFID scanner. By default, only basic Settings are
shown here. To show advanced settings, tap on the main app title 5 times.

## Developer Notes:

This project is a Xamarin application, made to be built with MS Visual Studio 2019 or from the command line using 
`msbuild` and `dotnet` (both of which come with Visual Studio). It's using .NET version 5.0.2 and Mono to run on 
Android / Linux / macos.

### Building from the command prompt

  - `nuget restore` to make sure all packages are properly fetched
  - `msbuild /p:AndroidBuildApplicationPackage=true /p:Configuration=Release /t:Rebuild /verbosity:normal UpwardFarms.Scantron.sln` 
    to actually build a Release

### Testing from the command prompt:

  - `dotnet test --configuration UnitTesting`

### Nuget Packages

Nuget should fetch all packages automatically for you. In the event that it does not, right-click the `Solution` and 
select `Manage Nu-Get Packages...`. Add the following packages. Rebuild.

#### Packages for General Application:

 - Tsl.AsciiProtocol.Std
 - Microsoft.Net.HTTP
 - Newtonsoft.Json
 - Xamarin.Forms
 - Xamarin.Forms.InputKit

#### Specifically for Android:

  - Xamarin.Android.Support.Design
  - Xamarin.Android.Support.v7.AppCompat
  - Xamarin.Android.Support.v4
  - Xamarin.Android.Support.v7.CardView
  - Xamarin.Android.Support.v7.MediaRouter

#### Additional Packages for Testing:

 - xunit
 - xunit.runner.visualstudio
 - Microsoft.Net.Test.Sdk
