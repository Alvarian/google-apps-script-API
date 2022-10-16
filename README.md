# Instructions
[Install python 3+](https://www.python.org/) and [pip](https://pypi.org/project/pip/) into your device. Also [install and sign up to ngrok](https://ngrok.com/) to tunnel this app's local URL to be used by google apps script.

Begin the server:
```bash
python app.py
```

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
Run "getGuessedGender" as the main point of starting the script.


:octocat:

<!-- https://dvj70ijwahy8c.cloudfront.net/DataFormatter/icon | [{"description": "In the google scripts editor, it uses Javascript to automate tasks. Here is a function that sends data from the spreadsheet to my API written in python to begin formatting.", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_3"}, {"description": "This function is calling the first one responsible for the API call, giving specific data and indicating the type of formatting desired. The return is then used to overwrite the previous data.", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_2"}, {"description": "This is the sheet before starting the task.", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_1"}, {"description": "Choosing the task to guess genders based on first name, this would be the end result", "image": "https://dvj70ijwahy8c.cloudfront.net/DataFormatter/slides/slide_image_0"}] -->


