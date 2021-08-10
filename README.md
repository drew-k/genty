# Genty

Genty is a general-purpose Discord bot with a wide variety of functionality.

## Token
For Genty's safety, the token is stored in a file ".env" which is accessed at runtime. Anyone who wishes to create their own version of Genty will have to create the same file (in the same directory) to store the token with the key "TOKEN".

## Prefixes

Genty stores individual prefixes for each guild in a json file. Upon joining a guild, Genty sets the default prefix as '%'. This can be changed later and will be updated in the bots memory. When Genty is removed from a guild, it will wipe its memory of a guild's prefix.

## Modmail [IN DEVELOPMENT]

In the future, Genty will be able to help mods easily keep track of threads created by users about server issues.

## Custom VCs

Genty is able to easily setup a button that let's anyone create their own, personal, custom voice channel where they have the ability to change important parts of a voice channel, including the name, user limit, and the access.
