document
    .getElementById("submitButton")
    .addEventListener(
        "click", 
        generateConfigJson
    )

function hasNonNull (array) {
    for (const el of array) {
        if (el != "") {
            return true;
        }
    }
    return false;
}

function allNonNull (array) {
    for (const el of array) {
        if (el === "") {
            return false;
        }
    }
    return true;
}

function getDydxRunEnvironment () {
    // IF YOU CHANGE THE RADIO, THEN CHANGE THE DYDX ENVIRONMENT TOO!
    // find if dydx run environment is test or mainnet
    if ( document.getElementById("dydxEnvMainnet").checked ) {
        return "mainnet";
    } else {
        return "testnet";
    }
}

function getAllInputs () {
    allInputs = {
        dydxKey: document.getElementById("dydxKey").value,
        dydxSecret: document.getElementById("dydxSecret").value,
        dydxPassphrase: document.getElementById("dydxPassphrase").value,
        senderEmailAddress: document.getElementById("senderEmailAddress").value,
        senderEmailPassword: document.getElementById("senderEmailPassword").value,
        toEmailAddress: document.getElementById("toEmailAddress").value,
        slackWebhookUrl: document.getElementById("slackWebhookUrl").value,
        discordWebhookUrl: document.getElementById("discordWebhookUrl").value,
        telegramBotToken: document.getElementById("telegramBotToken").value,
        telegramChatId: document.getElementById("telegramChatId").value,
        maxLeverageTrigger: document.getElementById("maxLeverageTrigger").value
    }

    Object.keys(allInputs).map(function(key, index) {
        allInputs[key] = allInputs[key].replace('&amp;','&');
      });

    return allInputs
}

function checkCleanInputs (allInputs) {
    // return true iff all inputs are clean

    // dydx
    const dydxConfig = [
        allInputs["dydxKey"],
        allInputs["dydxSecret"],
        allInputs["dydxPassphrase"]
    ]
    if ( ! allNonNull(dydxConfig) ) {
        alert("All of the dYdX parameters must be filled out!");
        return false;
    }
    
    // email
    const emailConfig = [
        allInputs["senderEmailAddress"],
        allInputs["senderEmailPassword"],
        allInputs["toEmailAddress"]
    ]
    if (
        hasNonNull(emailConfig) &&
        ! allNonNull(emailConfig)
    ) {
        alert("If you use want to use an email bot, then you must enter all of its parameters!");
        return false;
    }

    const telegramConfig = [
        allInputs["telegramBotToken"],
        allInputs["telegramChatId"],
    ];
    if (
        hasNonNull(telegramConfig) &&
        ! allNonNull(telegramConfig)
    ) {
        alert("If you use want to use the telegram bot, then you must enter all of its parameters!");
        return false;
    }

    return true;
}

function generateConfigJson () {
    console.log(
        "here!",
        getDydxRunEnvironment()
    );
    const allInputs = getAllInputs();
    const inputsAreClean = checkCleanInputs(allInputs);
    if (inputsAreClean) {
        console.log("All inputs are clean!")
        
        // Fill messenger blob json
        const messengerBlobJson = generateMessengerBlobJson(allInputs);
        document.getElementById("messengerBlobText").innerHTML = messengerBlobJson;
        
        
        // Fill api credential json
        const apiCredentialsJson = generateApiCredentialsJson(allInputs);
        document.getElementById("apiCredentialsText").innerHTML = apiCredentialsJson;

    }
    
}

function copyObject (source) {
    return JSON.parse(JSON.stringify(source));
} 

function myStringify (obj) {
    // stringify such that a json blob is well-formatted
    return JSON.stringify(obj, null, 4)
}

function generateMessengerBlobJson (userInputsObject) {
    var allMessengerBlobs = [];
    const dydxRunEnvironment = getDydxRunEnvironment();
    const baseMessengerBlob = {
        user_id: "0",
        dydx_config: {
            environment: dydxRunEnvironment
        },
        message_platform_config: {
            message_platform: "",
            api_key_config_id: 0,
            platform_specific_config: {}
        },
        event_trigger_config: {
            trigger: "below_thresh",
            trigger_options: {
                collateral_trigger_pct: JSON.stringify(100 / parseFloat(userInputsObject["maxLeverageTrigger"]))
            }
        }
    }
    
    // email
    const emailConfig = [
        userInputsObject["senderEmailAddress"],
        userInputsObject["senderEmailPassword"],
        userInputsObject["toEmailAddress"]
    ]
    if (
        allNonNull(emailConfig)
    ) {
        var emailMessengerBlob = copyObject(baseMessengerBlob);
        emailMessengerBlob["message_platform_config"]["message_platform"] = "email";
        emailMessengerBlob["message_platform_config"]["platform_specific_config"] = {to_email_address: userInputsObject["toEmailAddress"]};
        allMessengerBlobs.push(emailMessengerBlob);
    }

    // slack
    if (userInputsObject["slackWebhookUrl"] != "") {
        var slackMessengerBlob = copyObject(baseMessengerBlob);
        slackMessengerBlob["message_platform_config"]["message_platform"] = "slack";
        allMessengerBlobs.push(slackMessengerBlob)
    }

    // discord
    if (userInputsObject["discordWebhookUrl"] != "") {
        var discordMessengerBlob = copyObject(baseMessengerBlob);
        discordMessengerBlob["message_platform_config"]["message_platform"] = "discord";
        allMessengerBlobs.push(discordMessengerBlob)
    }

    // telegram
    const telegramConfig = [
        userInputsObject["telegramBotToken"],
        userInputsObject["telegramChatId"]
    ]
    if (allNonNull(telegramConfig)) {
        var telegramMessengerBlob = copyObject(baseMessengerBlob);
        telegramMessengerBlob["message_platform_config"]["message_platform"] = "telegram";
        allMessengerBlobs.push(telegramMessengerBlob)
    }
    
    return myStringify(allMessengerBlobs);
}

function generateApiCredentialsJson (userInputsObject) {
    var allApiCredentials = {
        "0": {

        }
    }
    // dYdX
    const dydxConfig = [
        userInputsObject["dydxKey"],
        userInputsObject["dydxSecret"],
        userInputsObject["dydxPassphrase"]
    ]
    if ( allNonNull(dydxConfig) ) {
        // technically it should be impossible to get to this stage if the dydx config hasn't been set yet
        // so this conditional may be unnecessary. However, we're still defensive, just in case!
        allApiCredentials["0"]["dydx"] = [{
            "key": userInputsObject["dydxKey"],
            "secret": userInputsObject["dydxSecret"],
            "passphrase": userInputsObject["dydxPassphrase"]
        }]
    } else {
        throw Error("Got to generating api_credentials.json when dydx API config isn't fully filled out!")
    }

    // email
    const emailConfig = [
        userInputsObject["senderEmailAddress"],
        userInputsObject["senderEmailPassword"],
        userInputsObject["toEmailAddress"]
    ]
    if (
        allNonNull(emailConfig)
    ) {
        allApiCredentials["0"]["email"] = [{
            "from_email_address": userInputsObject["senderEmailAddress"],
            "from_email_password": userInputsObject["senderEmailPassword"]
        }]
    }
    
    // slack
    if (userInputsObject["slackWebhookUrl"] != "") {
        allApiCredentials["0"]["slack"] = [{
            "webhook_url": userInputsObject["slackWebhookUrl"]
        }]
    }

    // discord
    if (userInputsObject["discordWebhookUrl"] != "") {
        allApiCredentials["0"]["discord"] = [{
            "webhook_url": userInputsObject["discordWebhookUrl"]
        }]
    }

    // telegram
    const telegramConfig = [
        userInputsObject["telegramBotToken"],
        userInputsObject["telegramChatId"]
    ]
    if (allNonNull(telegramConfig)) {
        allApiCredentials["0"]["telegram"] = [{
            "bot_token": userInputsObject["telegramBotToken"],
            "telegram_chat_id": userInputsObject["telegramChatId"]
        }]
    }

    // console.log("allAPiCreds", allApiCredentials)

    return myStringify(allApiCredentials);
}

// Handle copying of the JSON config files
function copyTextToClipboard(text) {
    if (!navigator.clipboard) {
        // fallbackCopyTextToClipboard(text);
        alert("Clipboard unavailable. You must copy the text manually.")
        return false;
    }
    navigator.clipboard.writeText(text).then(function() {
            console.log('Async: Copying to clipboard was successful!');
        }, function(err) {
        console.error('Async: Could not copy text: ', err);
        return false;
    });
    
    return true;
}

// messenger blob
document
    .getElementById("copyMessengerBlobButton")
    .addEventListener(
        "click", 
        () => {
            const config = document.getElementById("messengerBlobText").innerHTML;
            const didCopyText = copyTextToClipboard(config);
            if (didCopyText) {
                document.getElementById("messengerBlobsCopyComplete").innerHTML = "Messenger Blobs Copied!";
            }
        }
    )

// api credentials
document
    .getElementById("copyApiCredsButton")
    .addEventListener(
        "click", 
        () => {
            const config = document.getElementById("apiCredentialsText").innerHTML;
            const didCopyText = copyTextToClipboard(config);
            if (didCopyText) {
                document.getElementById("apiCredsCopyComplete").innerHTML = "API Credentials Copied!";
            }
        }
    )