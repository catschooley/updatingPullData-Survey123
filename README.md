# updatingPullData-Survey123
A template for updating the 'Pull Data' of the 'Media' folder in Survey123 using a Google Sheet shared in Google Drive. This template will pull in the new pull data as a csv, clean it from any whitespaces, commas, etc., then replace the pull data file currently used by the survey. A notification email is sent that this process has been completed. 

This code was written using inspiration and templating from Esri's Update Media Folder Python Script which can be found [here](https://survey123.maps.arcgis.com/home/item.html?id=521168944ace40d0827991eeeba03689)

Additions include:

* Pulling from Google Drive instead of a local source
* Cleaning of the CSV data
* Email Notifications
* Detailed explanation of new and existing processes
