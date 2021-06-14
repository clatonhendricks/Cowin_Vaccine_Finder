# :syringe: CoWin Vaccine Finder :syringe:

The intention of this repo is to help you to find a vaccine in India. 
A portion of this script is taken from [Uditvashisht](https://github.com/uditvashisht/cowin-email-alerts) repo. His repo contains the script that will help you to find the vaccine and email it to you but you need have Python installed and know how to use it. 
This repo release is self contained and does not have any dependencies. 

**NOTE:** You can only use this tool if you in India or use a VPN to connect to India. This is due to the limitation set by the API released by the Indian government."

## Usage 
Download the tool here and unzip the files. This only supports Windows and has been tested on Windows 10

This is a command line tool and you need to provide a list of pincodes that you want to search for vaccine. e.g. below

**Cowin_vaccine_finder.exe --pincodes 387001 387002**

After this executes, you will see a list of centers that have availabilty and the cost of vaccine (if any)

<Snapshot here>

This tool creates the following files 
**Vaccine_Availablity.txt** -> This file only gets created if there are vaccine slots available (See screenshot below)

**cowin_vaccine_finder.log** -> log file, contains a list of logger messages including a list of vaccine location even if there is no avaialability

Try to limit the pincodes to less than 3. 

# Screenshot 
![image of vaccine screenshot](https://github.com/clatonhendricks/Cowin_vaccine_finder/blob/main/Vaccine_screenshot.jpg?raw=true)

**Note: You can only run this tool from India as its API are blocked to query are blocked.** 
  
  
# Want to automatically search for vaccines?
You can use the "Task Scheduler" in Windows to run this tool every hour or every day. Follow the instructions below
  
	1. Click on Search in Windows and search for "Task Scheduler" and click on it
	2. Right click on "Task Scheduler Libary"
	3. Click on "Create task"
	4. Under first tab "General" - Enter any name that you can rememeber e.g. Vaccine Finder
	5. Go to the next tab "Triggers" and click on New - this is where you can set the schedule to run every hour or every day
	6. Select "Daily" and check "Repeat task every "1 hour" for a duration of "Indefinitely" and click OK
	7. Go to the next tab " Actions" and "Browse" to the folder where you can unzipped the **cowin_vaccine_finder.exe** and select it
	8. Under "Add arguments (optional)" - write the pincodes you want to search for e.g. **--pincodes 387001 560043**
	9. And that’s it, Click OK and you are done. Now this tool will run every hour and will try to find vaccines for you. 


## License
© 2021 Claton Hendricks
This repository is licensed under the GNU GPLv3 license. See LICENSE for details.
