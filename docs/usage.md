# Usage
*How to run a liquidation alert bot.*

## Method 1: Run from Docker (recommended)
1. Create a cloud virtual machine. If you've never done this before, follow the steps in the ["Running a Virtual Machine on Digital Ocean" guide](./cloud-vm).
2. To get the virtual machine set up, run the following in your virtual machine terminal:
    ```bash
    git clone https://github.com/maxholloway/dydx-alerts \
    && cd dydx-alerts \
    && bash scripts/setup-docker
    ```
3. You must provide dYdX credentials in order for the bot to run, and for every messaging platform that you want to send messages, you must acquire its API credentials as well. Use [dydxalerts.com](https://dydxalerts.com/) alongside the ["Getting Bot Config Credentials" guide](bot_config_credentials.md) to generate your bot credentials. 
4. Once `messenger_blobs.json` and `api_credentials.json` text are generated on dydxalerts.com, go back to your virtual machine terminal. On your virtual machine, run `nano messenger_blobs.json`, paste the contents of `messenger_blobs.json` from dydxalerts.com, then press the `Control` and `X` keys on your keyboard at the same time. When it asks you to save the modified buffer, type `Y`, then press enter when it asks about the file name. Do the same for your API credentials by entering the following into your terminal: `nano api_credentials.json`, then pasting the contents of `api_credentials.json` from dydxalerts.com, then exiting in the same way as before.
5. Run the following command:
    ```bash
    bash scripts/run-forever-docker
    ```
    This should give a long (64 character) string output that looks something like `3a7129e3962607...a7e6`. Check that the bot is running by running the command `docker ps`; you should see a `CONTAINER ID` that matches the first 12 characters of the previous string output, e.g. `3a7129e39626`. If there are no containers present, then something went wrong. To check the bot's logs, run the command `nano logs/logs.log`; any runtime errors will appear there.
6. It is now safe for you to type `exit` and close your terminal window. However, if your virtual machine turns off or if this docker daemon is otherwise interrupted, then you will need to re-run the `run-forever-docker` command above.

**YouTube Video Tutorial**

[![](https://img.youtube.com/vi/Kvo_Dt-4VNI/0.jpg)](https://www.youtube.com/watch?v=Kvo_Dt-4VNI)


## Method 2: Run from Source (for developers)
1. Create a cloud virtual machine. If you've never done this before, follow the steps in the ["Running a Virtual Machine on Digital Ocean" guide](./cloud-vm).
2. To get the virtual machine set up, run the following in your virtual machine terminal: 
    ```bash
    git clone https://github.com/maxholloway/dydx-alerts && cd dydx-alerts && bash scripts/setup
    ```
3. You must provide dYdX credentials in order for the bot to run, and for every messaging platform that you want to send messages, you must acquire its API credentials as well. Use [dydxalerts.com](https://dydxalerts.com/) alongside the ["Getting Bot Config Credentials" guide](bot_config_credentials.md) to generate your bot credentials. 
3. Use [dydxalerts.com](https://dydxalerts.com/) to generate your bot configuration. Once generated, download `api_credentials.json` and `messenger_blobs.json` to your computer. Now on your virtual machine, run `nano messenger_blobs.json`, paste the contents of `messenger_blobs.json` from your local computer, then press the `Control` and `X` keys on your keyboard at the same time. When it asks you to save the modified buffer, type `Y`, then press enter when it asks about the file name. Do the same for your API credentials by entering the following into your terminal: `nano api_credentials.json`, then pasting the contents of `api_credentials.json` from your local computer, then exiting in the same way as before.
4. Once `messenger_blobs.json` and `api_credentials.json` text are generated on dydxalerts.com, go back to your virtual machine terminal. On your virtual machine, run `nano messenger_blobs.json`, paste the contents of `messenger_blobs.json` from dydxalerts.com, then press the `Control` and `X` keys on your keyboard at the same time. When it asks you to save the modified buffer, type `Y`, then press enter when it asks about the file name. Do the same for your API credentials by entering the following into your terminal: `nano api_credentials.json`, then pasting the contents of `api_credentials.json` from dydxalerts.com, then exiting in the same way as before.
5. Type the command `screen` and press enter. Now enter the following command, which will run the bot for as long as the virtual machine is active.
    ```bash
    source venv/bin/activate && bash scripts/run-forever
    ```
    To check the bot's logs, run the command `nano logs/logs.log`; any runtime errors will appear there.
6. Finally, press "Control"+"A" at the same time, then "Control"+"D" at the same time. This takes you back to the terminal that you had before you entered the screen command. It is now safe for you to type `exit` and close your terminal window.
