# Genty

[![Bot Status](https://top.gg/api/widget/status/873165810171002881.svg?noavatar=true)](https://top.gg/bot/873165810171002881)
[![CodeFactor](https://www.codefactor.io/repository/github/drew-k/genty/badge)](https://www.codefactor.io/repository/github/drew-k/genty)
[![Version](https://img.shields.io/github/v/release/drew-k/genty?include_prereleases)](https://github.com/drew-k/genty/releases)
[![Support Server](https://img.shields.io/discord/960915291502686298)](https://discord.gg/a8qwkJvshH)

## Requirements

To self-host, you will need the following:

* [python](https://www.python.org/downloads/)
* [git](https://git-scm.com/downloads)
* [disnake](https://github.com/DisnakeDev/disnake)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

**python** comes preinstalled on some operating systems.

## Installation

Clone repository

```text
git clone https://github.com/drew-k/genty.git
```

Install modules in requirements.txt

```text
pip install -r requirements.txt
```

Create an environment variable with your bot's token:

```text
// Windows
set TOKEN=[your_token_here]

// Linux & MacOS
export TOKEN=[your_token_here]
```

Start the bot
```text
cd src
python bot.py
```

## Updating

To update:

```text
git pull origin master
```

## Finding your Token
Go to the [Discord Application Page](https://discord.com/developers/applications/) and create a new application. First,
go to the `Bot` tab and find your token (should be under your Bot name). Next, navigate to the `OAuth2` tab and 
check the following:

* bot
* applications.commands
* Administrator

## Usage

List of commands:

| Command                     | Permission       | Description                          |
|-----------------------------|------------------|--------------------------------------|
| .load \<filepath\>          | Bot owner        | Loads a new extension                |
| .unload \<filepath\>        | Bot owner        | Unloads an extension                 |
| /wipe \<n\>                 | `ADMINISTRATOR`  | Deletes 'n' messages                 |
| /uptime                     | Bot owner        | Gets the current uptime of the bot   |
| /rps \<stats:True or False\>| Anyone           | Play rps with the bot and check stats|

`/load` and `/unload` both expect a file path in format `dir.module` such as `extensions.slash_commands`

Commands in `src/extensions/custom_vc.py`:

| Command                                | Permission       | Description                                                               |
|----------------------------------------|------------------|---------------------------------------------------------------------------|
| /vc_whitelist \<Optional: member\>     | Channel owner    | Whitelists a user to a custom channel                                     |
| /vc_blacklist \<Optional: member\>     | Channel owner    | Blacklists a user from a custom channel                                   |
| /vc_limit \<Optional: n\>              | Channel owner    | Sets a user limit of `n` on the custom channel                            | 
| /vc_rename \<Optional: name\>          | Channel owner    | Renames a custom channel to `name`                                        |
| /vc_lock                               | Channel owner    | Locks a custom channel (whitelisted users can still join)                 |
| /vc_unlock                             | Channel owner    | Unlocks a custom channel (default setting, blacklisted users cannot join) |


## Invite bot to your server

Click [here](https://discord.com/api/oauth2/authorize?client_id=873165810171002881&permissions=8&scope=applications.commands%20bot) 
to invite this bot to your server. 

## Authors

This bot was made by [drew-k](https://github.com/drew-k) &
[virusv2](https://github.com/virusv2)

[Contributors](https://github.com/drew-k/genty/graphs/contributors)

## License

Genty is licensed under the MIT license.
