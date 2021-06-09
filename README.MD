# :syringe: CoWin Vaccine Finder :syringe:

The intention of this repo is to help you to find a vaccine in India.
The majority of this script is taken from [Uditvashisht](https://github.com/uditvashisht/cowin-email-alerts) repo. His repo contains the script that will help you to find the vaccine and email it to you but you need have Python installed. 

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

**Note: You can only run this tool from India as its API are blocked to query are blocked. 

## License
© 2021 Claton Hendricks
This repository is licensed under the GNU GPLv3 license. See LICENSE for details.
