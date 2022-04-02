# Genty

Multipurpose Discord bot built to make your life easier. 

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

Place your token in an environment variable (.env) in the root directory with the following syntax:

```text
TOKEN=[your_token_here]
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

| Command                   | Permission       | Description                          |
|---------------------------|------------------|--------------------------------------|
| /load \<filepath\>        | Bot owner        | Loads a new extension                |
| /unload \<filepath\>      | Bot owner        | Unloads an extension                 |
| /reload \<filepath\>      | Bot owner        | Reloads an extension                 |
| /wipe \<n\>               | `ADMINISTRATOR`  | Deletes 'n' messages                 |
| /uptime                   | Bot owner        | Gets the current uptime of the bot   |

Commands in `src/extensions/custom_vc.py`:

| Command                             | Permission       | Description                                                               |
|-------------------------------------|------------------|---------------------------------------------------------------------------|
| /whitelist \<Optional: member\>     | Channel owner    | Whitelists a user to a custom channel                                     |
| /blacklist \<Optional: member\>     | Channel owner    | Blacklists a user from a custom channel                                   |
| /limit \<Optional: n\>              | Channel owner    | Sets a user limit of `n` on the custom channel                            | 
| /rename \<Optional: name\>          | Channel owner    | Renames a custom channel to `name`                                        |
| /lock                               | Channel owner    | Locks a custom channel (whitelisted users can still join)                 |
| /unlock                             | Channel owner    | Unlocks a custom channel (default setting, blacklisted users cannot join) |


## Invite bot to your server

Click [here](https://discord.com/api/oauth2/authorize?client_id=873165810171002881&permissions=8&scope=applications.commands%20bot) 
to invite this bot to your server. 

## Authors

This bot was made by [drew-k](https://github.com/drew-k).

[Contributors](https://github.com/drew-k/genty/graphs/contributors)

## License

Genty is licensed under the MIT license.