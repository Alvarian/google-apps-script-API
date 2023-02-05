![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)
![](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
***

# Introduction
This project is an API catered to google sheet via google apps script. It handles common and repetitive formatting tasks thats usually in demand for demographic type data.

## Getting Started
[Install python 3+](https://www.python.org/) and [pip](https://pypi.org/project/pip/) into your device. After pip is installed in your computer, we need flask to continue, so in your terminal run:
```
pip install flask
python manage.py
```

## Expose app
In order for google apps script to request to the running application, the local endpoint needs to be forwarded and exposed to the web using ![ngrok](). Follow the intructions until usage and run:
```
ngrok http 5000
```
Copy the "Forwarding" url, ex: https://7d0b-173-52-201-90.ngrok.io, to use in the next step.

## Usage
Log in to your google account and navigate to google sheets and in a new sheet fill one column with random first names with a column title of "Full Name". 

Go to the top tool bar > Extensions > AppSheet > Create an app.

Create a new sheet and put the following algorithms in it:
```
function callServer(columns, data, job)  {
    let draft = {
        columns,
        data
    };

    const URL = <YOUR_GENERATED_NGROK_URL>+job;

    let options = {
        method: "POST",
        contentType: "application/json",
        headers: {
            "Authorization": "bearer " + ScriptApp.getOAuthToken()
        },
        payload: JSON.stringify(draft),
        muteHttpExceptions: true
    };

    return urlFetchApp.fetch(URL, options);
}

function getGuessedGender() {
    const cs = getCurrentSheet();

    const res = JSON.parse(callServer(["first_name"], cs.rows, "genderize"));

    cs.sheet.get(1, 1, res.length, res[0].length).setValues(res);
}
```
`YOUR_GENERATED_NGROK_URL` is where you can paste the ngrok url, then run "getGuessedGender" as the main point of starting the script.

# References
* Flask (https://flask.palletsprojects.com/en/2.2.x/)
* Ngrok (https://ngrok.com/)
* Google Apps Script (https://developers.google.com/apps-script/guides/sheets/functions)
* JavaScript Fetch (https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)

:octocat:

<!-- https://dvj70ijwahy8c.cloudfront.net/DataFormatter/icon | [{"description": "In the google scripts editor, it uses Javascript to automate tasks. Here is a function that sends data from the spreadsheet to my API written in python to begin formatting.", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_3"}, {"description": "This function is calling the first one responsible for the API call, giving specific data and indicating the type of formatting desired. The return is then used to overwrite the previous data.", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_2"}, {"description": "This is the sheet before starting the task.", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_1"}, {"description": "Choosing the task to guess genders based on first name, this would be the end result", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_0"}] -->


