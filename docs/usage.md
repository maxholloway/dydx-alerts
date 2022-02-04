# Usage
*How to run a liquidation alert bot.*

## Method 1: Run from Docker (recommended)
1. Create a cloud virtual machine. If you've never done this before, follow the steps in the ["Running a Virtual Machine on Digital Ocean" guide](./cloud-vm).
2. To get the virtual machine set up, run the following in your virtual machine terminal:
    ```bash
    git clone https://github.com/maxholloway/dydx-alerts && cd dydx-alerts && bash setup-docker
    ```
3. Use [dydxalerts.com](dydxalerts.com) to generate your bot configuration. Once generated, download `api_credentials.json` and `messenger_blobs.json` to your computer. Now on your virtual machine, run `nano messenger_blobs.json`, paste the contents of `messenger_blobs.json` from your local computer, then press the `Control` and `X` keys on your keyboard at the same time. When it asks you to save the modified buffer, type `Y`, then press enter when it asks about the file name. Do the same for your API credentials by entering the following into your terminal: `nano api_credentials.json`, then pasting the contents of `api_credentials.json` from your local computer, then exiting in the same way as before.
4. Run the following command:
    ```bash
    docker run \
        -d \
        -v $(pwd)/messenger_blobs.json:/messenger_blobs.json \
        -v $(pwd)/api_credentials.json:/api_credentials.json \
        maxholloway/dydx-alerts:0.1.0
    ```
5. It is now safe for you to type `exit` and close your terminal window. However, if your virtual machine turns off or if this docker daemon is otherwise interrupted, then you will need to re-run the `docker run` command above.


## Method 2: Run from Source (for developers)
1. Create a cloud virtual machine. If you've never done this before, follow the steps in the ["Running a Virtual Machine on Digital Ocean" guide](./cloud-vm).
2. To get the virtual machine set up, run the following in your virtual machine terminal: 
    ```bash
    git clone https://github.com/maxholloway/dydx-alerts && cd dydx-alerts && bash setup
    ```
3. Use [dydxalerts.com](dydxalerts.com) to generate your bot configuration. Once generated, download `api_credentials.json` and `messenger_blobs.json` to your computer. Now on your virtual machine, run `nano messenger_blobs.json`, paste the contents of `messenger_blobs.json` from your local computer, then press the `Control` and `X` keys on your keyboard at the same time. When it asks you to save the modified buffer, type `Y`, then press enter when it asks about the file name. Do the same for your API credentials by entering the following into your terminal: `nano api_credentials.json`, then pasting the contents of `api_credentials.json` from your local computer, then exiting in the same way as before.
4. Type the command `screen` and press enter. Now enter the following command, which will run the bot for as long as the virtual machine is active.
    ```bash
    source venv/bin/activate && bash run-forever
    ```
5. Finally, press "Control"+"A" at the same time, then "Control"+"D" at the same time. This takes you back to the terminal that you had before you entered the screen command. It is now safe for you to type `exit` and close your terminal window.
