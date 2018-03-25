// Initialize Firebase
const config = {
    apiKey: "AIzaSyDWgGOZMOlalyCGIgHLzYw5KwqcFoBUqY4",
    authDomain: "kassiakarras-1fcbf.firebaseapp.com",
    databaseURL: "https://kassiakarras-1fcbf.firebaseio.com",
    projectId: "kassiakarras-1fcbf",
    storageBucket: "kassiakarras-1fcbf.appspot.com",
    messagingSenderId: "942270893396"
};

firebase.initializeApp(config);

const database = firebase.database();

let writeEmail = () => {

    let email = document.getElementById(`emailinput`).value;

    database.ref(`mailing_list`).push({

        email: email

    });
};

let getEmails = () => {

    const ref = database.ref(`mailing_list`);

    let emails = [];


    ref.on(`value`, function (snapshot) {
        snapshot.forEach(function (child) {

            emails.push(child.val()[`email`].toString());


        })
    });

    setTimeout(getEmails, 500);

    document.getElementById(`emaildata`).innerHTML = emails;

};

getEmails();