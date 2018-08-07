# AntiTeamFlash

## Introduction
AntiTeamFlash is a plugin created for [Source.Python](https://github.com/Source-Python-Dev-Team/Source.Python).  As such, it requires [Source.Python](https://github.com/Source-Python-Dev-Team/Source.Python) to be installed on your CS:S or CS:GO game server.  It currently only works on CS:GO, but will be updated for CS:S in the future.

This plugin stops players from being flashed by teammates.

<br>

## Installation
To install, simply download the current release from its [release thread](https://forums.sourcepython.com/viewtopic.php?t=895) and install it into the main directory for your server.

Once you have installed AntiTeamFlash on your server, simply add the following to your autoexec.cfg file:
```
sp plugin load anti_team_flash
```

<br>

## Configuration
After having loaded the plugin once, a configuration file will have been created on your server at **../cfg/source-python/anti_team_flash.cfg**

Edit that file to your liking.  The current default configuration file looks like:
```
// Default Value: 0
// Enable/Disable flashing the thrower of the flashbang.
   atf_flash_thrower 0


// Default Value: 1
// Enable/Disable flashing spectators.
   atf_flash_spectator 1


// Default Value: 1
// Enable/Disable flashing dead players.
   atf_flash_dead 1
```
