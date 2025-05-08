# ../anti_team_flash/config.py

"""Creates server configuration and user settings."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from config.manager import ConfigManager

# Plugin
from .info import info
from .strings import CONFIG_STRINGS

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "flash_dead",
    "flash_spectator",
    "flash_thrower",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the anti_team_flash.cfg file and execute it upon __exit__
with ConfigManager(info.name, "atf_") as config:

    # Create the thrower convar
    flash_thrower = config.cvar("flash_thrower", 0, CONFIG_STRINGS["Thrower"])

    # Create the spectator convar
    flash_spectator = config.cvar("flash_spectator", 1, CONFIG_STRINGS["Spec"])

    # Create the dead convar
    flash_dead = config.cvar("flash_dead", 1, CONFIG_STRINGS["Dead"])
