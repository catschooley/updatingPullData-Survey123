# # Cleaning Minerals Pull Data for Minerals Field Inspections

# Cat Schooley  
# GIS Analyst  
# November 5, 2021
# 
# ### Using Pull Data

### import modules ###

import pandas as pd



### Remember the url format ###

# "https://docs.google.com/spreadsheets/d/{SPREADSHEETID}/export?format=csv&id{SPREADSHEETID}&gid=2113599541"


###### Uncomment this section to use URL instead of Google Drive Desktop ######

# url = "https://docs.google.com/spreadsheets/d/{SPREADSHEETIDENTIFIER}/export?format=csv&id{SPREADSHEETIDENTIFIER}&gid=2113599541"


# df = pd.read_csv(url, dtype = object, usecols= [3, 4, 5, 6, 7, 8, 9, 10, 11, 12], na_filter = False)

################################################################################



###### Comment out this section to use URL instead of Google Drive Desktop ######

file = '{MYGOOGLEDOC}.xlsm'


df = pd.read_excel(file, sheet_name="For Pull Data", dtype = str, usecols= [3, 4, 5, 6, 7, 8, 9, 10, 11, 12], na_filter = False, index_col= None)

########################################################################

# Ensure dataframe is read as a 'string'
df = df.astype(str)



##### Remove Whitespaces and commas #####


def whitespaceRemover(dataframe):
    
    # iterating over the columns
    for i in dataframe.columns:
          
        # checking datatype of each columns
        if dataframe[i].dtype == 'object': #helps pinpoint if something is wrong with the data type
              
            # applying strip function on column
            dataframe[i] = dataframe[i].map(str.strip)
            
            dataframe[i] = dataframe[i].str.replace(",","")
            
        else:
              
            # if condn. is False then it will do nothing.
            pass
            
            print(f"{i} was skipped because field value was not a string")
        
### End Function ###

print("Commas and whitespaces being removed...")

whitespaceRemover(df) # plug your dataframe into function


##### Overwriting Pull Data #####


print("Overwriting old Minerals Pulldata with cleaned Minerals Pulldata...")

df.to_csv(r"C:\Users\cschooley\ArcGIS\My Survey Designs\PullUpdate\MineralsPulldata.csv", index = False) 


# #### Replacing Online Survey123 Pull Data with Local Update
# 
# To start we will import the required modules and define our variables.<br>
# **Please format folder directories as C:/Users/username… include a trailing slash after the final folder name as the updated file directory is concatenated to the updated file name**
# 
# 
# The variables are defined as follows: 
# 
# * **portalURL** - The URL for your WebGIS Portal (ex. www.arcgis.com)
# * **username** - Your WebGIS Portal username (ex. gisadmin)
# * **password** - You WebGIS Portal password (ex. gisadmin1)
# * **itemID** - The Item ID for the ArcGIS Survey123 Form Item in you WebGIS Portal (ex. 89bc8c7844e548e09baa3aad4695e78b)
# * **download_folder** - The folder directory you would like the Survey123 Form Item to be downloaded with the trailing slash (ex. C:/temp/)
# * **updated_file** - The updated file name containing the extension (ex. pullData.csv)
# * **source_loc** - Folder directory where the updated file is located (ex. C:/users/username/arcgis/my survey designs/)



### Modules ###

import arcgis
from arcgis.gis import GIS
import zipfile
import shutil
import arcpy
import os

token = arcpy.GetSigninToken()
if token is not None:
    print(token['token'])

portalURL = r'https://arcgis.com'
username = 'username'
password = 'password'
itemID = 'itemID'  
download_folder = r'C:/temp/'
updated_file = r'pullData.csv'
source_loc = r'C:\Users\cschooley\ArcGIS\My Survey Designs\PullUpdate/'# this is where mine is saved. PullUpdate is a custom folder I added


### Connect to GIS ###

gis = GIS(portalURL, username, password, verify_cert=False)


# #### Download the survey
# 
# We will start by grabbing the properties of the Survey123 Form Item.
# These properties are used later when we update the Form Item with a zip file
# containing the new media content.

survey_manager = arcgis.apps.survey123.SurveyManager(gis)
surveyId = survey_manager.get(itemID)
surveyProp = surveyId.properties

# Find the Form item in the gis and download as a zip file to the
# *download_folder* directory.

itm = arcgis.gis.Item(gis,itemID)
print(itm)
savedZip = itm.download(save_path=download_folder)


# Extract the zip file to an *`_extracted`* folder in the download location.
# This *`_extracted`* folder is where the updated media files will be copied
# and rezipped later on. 

def extractZIP(filename,folder):
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(folder)

extractZIP(savedZip, download_folder + "_extracted/")


# Copy the updated file to the media folder replacing the old file. 


source_file = source_loc + updated_file
dest_file = download_folder + "_extracted/esriinfo/media/" + updated_file
shutil.copyfile(source_file, dest_file)
print (updated_file + " updated to: " + download_folder + "_extracted/esriinfo/media/")


# Delete the old zip file that was previously downloaded. This will prevent any namespace issues and ensure the process of zipping and uploading the updated survey goes smoothly. 


os.remove(savedZip)
print ("Old zip file deleted from: " + download_folder)


##### Upload the updated survey #####


zipFileName = surveyProp['title']
os.chdir(download_folder)
updateZip = shutil.make_archive(zipFileName, 'zip', download_folder + '_extracted/')
print (updateZip)


# Upload the new zip file and update the Form Item with the new Media folder content.

# Then, clean up intermediate data. This process will delete the updated zip file as well as the extracted folder containing the unzipped survey content.


itm.update({},updateZip)

os.remove(updateZip)
print (zipFileName + " deleted from: " + download_folder)

shutil.rmtree(download_folder + "_extracted/")
print ("extracted folder deleted from: " + download_folder)
print (zipFileName + " successfully updated with " + source_file + " and uploaded to your ArcGIS portal!")


###### Send Email Notifications ######

### Modules ###

import yagmail
from datetime import date
from datetime import datetime

print("Sending Emails...")
now = datetime.now()
date = now.strftime("%m/%d/%Y")
time = now.strftime("%I:%M:%S %p")
reciever = ['email1', 'email2', 'email3']
body = f'Hello,\n\n The {zipFileName} survey successfully updated with the latest Pulldata available as of {date} and uploaded to the {username}'s' account!\n\nCompleted on {date} at {time}.\n\nThank you!'
yag = yagmail.SMTP("email", 'password')
for recipient in reciever:
    yag.send(
        to=recipient,
        subject='subject',
        contents = body
    )

print('Emails sent successfully.')
