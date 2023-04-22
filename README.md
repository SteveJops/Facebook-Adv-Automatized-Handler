
# Facebook Advertisement Handler

Instrument for handling your business Facebook page advertisement with ability to get, add and remove your adv apps. Also can get the whole list of your fb created apps.


## Installation

- Clone or download the script from github.

- Install python 3.10

- Install Docker

- Enter written below commands

```bash
    git clone https://github.com/SteveJops/Facebook-Adv-Automatized-Handler.git 
    cd cloned repository
    change your ip in main.py in selenoid settings to get successful using Selenium in Docker
    change your settings either in docker file nor docker-compose.yml
    docker-compose up
```

- Enter your request in browser (default = https://localhost:8008) to interact with the api

Be using the script.
## Usage/Examples

There are default url to interact with:

(Before, also need to change your fb acc settings to login)


- your_host/apps - to get the whole list of your created developer api


- your_host/add/{app_id} - to have being added your adv app to main list


- your_host/{app_id} - to get, if available, app`s advertising ids list


- your_host/remove/{app_id} - to have being removed your adv app to main list
