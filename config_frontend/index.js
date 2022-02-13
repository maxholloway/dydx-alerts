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

function matches (string, regex) {
    // Return True if string matches regex, else return False
    if (typeof string == "number") {
        string = string.toString()
    }

    const matches = string.match(regex)
    if ((matches === null) || (matches.length != 1)) {
        return false;
    } else {
        return (matches[0].length == string.length)
    }
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
    } else if (!matches(
        allInputs["dydxKey"], 
        /[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}/
        )) {
        alert("Invalid dYdX API 'key'.");
        return false;
    } else if (!matches(
        allInputs["dydxSecret"], 
        /[\w-]{40}/
        )) {
        alert("Invalid dYdX API 'secret'.");
        return false;
    } else if (!matches(
        allInputs["dydxPassphrase"], 
        /[\w-]{20}/
        )) {
        alert("Invalid dYdX API 'passphrase'.");
        return false;
    }
    
    // email
    const emailConfig = [
        allInputs["senderEmailAddress"],
        allInputs["senderEmailPassword"],
        allInputs["toEmailAddress"]
    ]
    if (hasNonNull(emailConfig)) {
        if (! allNonNull(emailConfig)) {
            // might not be necessary, since we do regex checks, but still helpful
            alert("If you use want to use an email bot, then you must enter all of its parameters!");
            return false;
        } else if (!matches(allInputs["senderEmailAddress"], /[\w-]+@[\w-]+.[\w-]+/)) {
            alert("Invalid sender email address.")
            return false;
        } else if (!matches(allInputs["senderEmailPassword"], /.+/)) {
            alert("Invalid sender password.")
            return false;
        } else if (!matches(allInputs["toEmailAddress"], /[\w-]+@[\w-]+.[\w-]+/)) {
            alert("Invalid receiver email address.")
            return false;
        }
        
    }

    // slack
    if (hasNonNull([allInputs["slackWebhookUrl"]])) {
        if (!matches(allInputs["slackWebhookUrl"], /https:\/\/hooks.slack.com\/services\/[\w]{11}\/[\w]{11}\/[\w]{24}/)) {
            alert("Invalid slack webhook url.");
            return false;
        }
    }

    // discord
    if (hasNonNull([allInputs["discordWebhookUrl"]])) {
        if (!matches(allInputs["discordWebhookUrl"], /https:\/\/discord.com\/api\/webhooks\/[\w]+\/[\w]+-[\w]+/)) {
            alert("Invalid discord webhook url.");
            return false;
        }
    }

    // telegram
    const telegramConfig = [
        allInputs["telegramBotToken"],
        allInputs["telegramChatId"],
    ];
    if (hasNonNull(telegramConfig)) {
        if (! allNonNull(telegramConfig)) {
            alert("If you use want to use the telegram bot, then you must enter all of its parameters!");
            return false;
        } else if (!matches(allInputs["telegramBotToken"], /[\d]{10}:[\w-]{35}/)) {
            alert("Invalid telegram bot token.")
            return false;
        } else if (!matches(allInputs["telegramChatId"], /[-]*[\d]{9}/)) {
            alert("Invalid telegram chat id.")
            return false;
        }
    }

    // max leverage
    var maxLeverage = allInputs["maxLeverageTrigger"]
    if (typeof maxLeverage != "number") {
        maxLeverage = parseFloat(maxLeverage);
    }
    
    if (isNaN(maxLeverage)) {
        alert("Invalid maximum leverage: unable to parse number.");
        return false;
    } else if (maxLeverage <= 0) {
        alert("Invalid maximum leverage: leverage must be positive.");
        return false;
    } else if (maxLeverage > 25) {
        alert("Invalid maximum leverage: leverage must be less than 25.");
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

var slider = document.getElementById('maxLeverageTrigger')
slider.onchange = function updateSlider() {
    document.getElementById("maxLeverageNumberDisplay").innerHTML = this.value
}