# dYdX Alerts
*Notifications for dYdX account info*

## Why use dYdX Alerts?
If you have ever been liquidated on dYdX, then you know just how valuable it is have a tool that notifies you before your account gets wrecked. This tool solves that problem by sending notifications on all popular messaging apps (discord, email, slack, telegram) before their positions are force-liquidated.

## How to use dYdX Alerts
The current version of dYdX Alerts requires users to host their own dYdX Alerts bot. To learn more about running your own bot, visit [the usage page in the docs](https://docs.dydxalerts.com/usage.html)

## FAQ

### Is dYdX Alerts secure?
In the current version of dYdX alerts, all code is hosted on the user's own computer or their cloud instance. **Nobody other than the user has access to user API credentials at any point.** Furthermore, the API credentials used for this bot are not sufficient for initiating withdrawals or placing orders on dYdX. The most that a malevolent actor can do with the API credentials provided is cancel the user's orders.

### Where is the documentation?
[Here](https://docs.dydxalerts.com/).

### I'm using windows ... how do I resolve issue X?
I am not a windows user, and I will have no idea how to answer it unless I can replicate it on a mac or linux machine. Still feel free to ask though!

### What message platforms do I have to choose from?
See all message platform docs [here](./docs/message_platforms.md).


### I have a question that isn't answered in this FAQ.
Feel free to open a GitHub issue.
