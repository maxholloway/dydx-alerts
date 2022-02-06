# Getting Bot Config Credentials

*Instructions for getting configuration details that are needed in order to run a bot. For any messaging platform that we support, you can follow the instructions below to retrieve the platform credentials that are necessary for the program to send messages. dYdX credentials are required.*

## Getting dYdX Credentials
Here are instructions for retrieving your dYdX API credentials from the dYdX website. You can follow these exact instructions in a chromium-based (e.g. Chrome, Brave) browser. If you are using a different browser, then inspecting web pages may require 

1. Go to [trade.dydx.exchange](https://trade.dydx.exchange/). If the wallet you want to use is not connected to dYdX yet, then click the "Connect Wallet" button and sign the Metamask transactions that dYdX requests from you. You should now see your portfolio value.
2. Right-click on any blank part of the page, and click "Inspect". If you are using a non-chrome web browser, use its inspect tool. Inside the "Inspect" window, find the tab that says "Application", then find "Local Storage" on the left-side of the panel, then click "trade.dydx.exchange" (or "trade.stage.dydx.exchnage" if on testnet). Finally, find where in the table that `Key` has the value `API_KEY_PAIRS`, click on that, and open it up. Find the wallet address that you want to track, and copy the value associated with "key", "passphrase", and "secret". ![](assets/dydx-credentials-workflow/copy-api-credentials.png)
3. Go to [dydxalerts.com](https://dydxalerts.com/) and paste the key, secret, and passphrase into the "dYdX Bot Config" section.

## Getting Gmail Credentials
*Prerequisites: None.*
dYdX Alerts supports email notifications through a gmail account (*it does not support other email providers currently*). To set up a new gmail account to send notifications, follow the steps below.

1. Create a new gmail account [here](https://accounts.google.com/signup). Do *not* enable 2-factor authentication.
2. Turn *Allow less secure apps to On* [here](https://myaccount.google.com/lesssecureapps). Note that the only "less secure app" that will use this email address is the bot that you yourself are running. ![](assets/email-credentials-workflow/less-secure-off.png)
3. Copy the email address and email password into the "Email Bot Config" section of [dydxalerts.com](https://dydxalerts.com/).


## Getting Slack Credentials
*Prerequisites: You must have administrator permissions on a slack workspace already.*
dYdX Alerts also supports notifications to slack channels through application webhooks. This requires setting up a Slack application and then creating a webhook on that application. Follow the steps below to set up slack notifications.

1. Go to the Slack API documentation on incoming webhooks ([link](https://api.slack.com/messaging/webhooks)). Once there, follow the instructions for creating a slack app by clicking "Create your Slack app". Then follow the following instructions to create the slack app. Click "Create New App", select "From Scratch", and give the app a name and choose the slack workspace where it should be deployed. Now you should land on a "Basic Information" page, which has an "Incoming Webhooks" option; click that. Now, on the webhook page, toggle the "Activate Incoming Webhooks" button. Scroll to the bottom of the page, and click "Add New Webhook to Workspace", and select the slack channel where you want the webhook to post. Once you finish making the new webhook, find the Webhook URL and copy it; it should look like something like `https://hooks.slack.com/services/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`.
2. Paste that Slack Webhook URL into the "Slack Bot Config" section of [dydxalerts.com](https://dydxalerts.com/).


## Getting Discord Credentials
*Prerequisites: You must have administrator permissions on a discord server already.*
1. Open the discord server where you would like to create a webhook.
2. In the list of channels for the discord server, hover over the discord channel you would like to add the webhook to. You should see a gear icon appear that says "Edit Channel". Click on that gear. ![](assets/discord-credentials-workflow/click-gear.png)
3. Go to "Integrations" tab, click "New Webhook", copy the Webhook URL, and click "Save Changes". The webhook URL should look something like `https://discord.com/api/webhooks/9...124/m...g2Z_9w`. ![](assets/discord-credentials-workflow/click-copy-then-save.png)
4. Paste that Discord Webhook URL into the "Discord Bot Config" section of [dydxalerts.com](https://dydxalerts.com/).

## Getting Telegram Credentials
*Prerequisites: You must have a Telegram account already.*
1. Open the telegram app, and create a DM chat with the user `@BotFather`. Create a new bot by sending BotFather the message `/newbot`. Follow the instructions sent to you by the BotFather to create give a name and username to the new bot. In the end, you should see that the bot has been created successfully, and you are given a token "to access the HTTP API". This is the bot's token. Keep this private. ![](assets/telegram-credentials-workflow/make-tg-bot.png)
2. Start a new group with your bot, or alternatively add it to one of your existing telegram groups. Once there, also invite [`@RawDataBot`](https://t.me/RawDataBot) to the group. Once added, `@RawDataBot` will send a message with a bunch of information. Find where it says `"chat": {"id": #########, "title": "...", ...}`, and copy the value associated with "id". It should look something like `-774568981`. This is your chat id. Once the chat id is copied, you can remove `@RawDataBot` from your telegram channel. ![](assets/telegram-credentials-workflow/start-group.png)
3. Go to [dydxalerts.com](https://dydxalerts.com/), and paste the telegram bot token and telegram chat id into their respective boxes.
