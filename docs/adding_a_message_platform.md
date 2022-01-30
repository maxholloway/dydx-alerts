# Adding a Message Platform

## Overview
Message platforms are simply locations where you might receive a message, such as Slack or Email. 

This repository was developed with a few message platforms built in, namely Discord, Email, Slack, and Telegram. To interact with a different platform (e.g. Whatsapp), you will to add support in this library for it.

Luckily, adding a message platform isn't too hard! This document serves as a developer's guide for adding a message platform to the repository.

## Step 0: Fork It!
Fork this repo and create a development branch on the fork.

## Step 1. Implement the Message Platform Class
* Inside `message_platform.py`, ceate a `<platform_name>MessagePlatform(BaseMessagePlatform)` class. This class must override an `async send_message()` function a function, which does precisely that: send messages! See `TelegramMessagePlatform` for an example.
* Add a clause to the conditional inside `get_message_platform(message_platform_config, message_api_credentials)`. This conditional is what converts the message platform name in `messenger_blobs.json` to the actual message platform object. In other words, it's the bridge between config and code. Nice!
* Write unit tests. <!-- TODO: create a unit testing framework -->

## Step 2: Update the Documentation
* Add the message platform name to the `messenger_blobs.schema` file as one of the "message_platform" property enum options. Without this step, nobody will be able to use the new platform. :(
* Add a description of the new trigger to `message_platforms.md`.

## Step 3: Add the Message Platform to the CLI
<!-- TODO: Create the CLI. -->

## Step 4: Test (Manually + Unit)
* Test the workflow manually to make sure the CLI works properly.
* Ensure that all unit tests pass

## Step 5: Submit PR
Submit a PR to the main repo!

