# ../anti_team_flash/anti_team_flash.py

"""Stops players from being flashed by teammates."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from config.manager import ConfigManager
from entities.hooks import EntityCondition
from entities.hooks import EntityPostHook
from entities.hooks import EntityPreHook
from memory import make_object
from players.entity import Player
from players.helpers import userid_from_index
from translations.strings import LangStrings
from weapons.entity import Weapon

# Plugin
from .info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create the team variable to check against later
_flashbang_team = None

# Create the thrower variable to check against later
_flashbang_thrower = None

# Get the config strings to use
config_strings = LangStrings(info.name)

# Store the flashbang condition
_is_flashbang = EntityCondition.equals_entity_classname('flashbang_projectile')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the config file
with ConfigManager(info.name, 'atf_') as config:

    # Create the thrower convar
    flash_thrower = config.cvar('flash_thrower', 0, config_strings['Thrower'])

    # Create the spectator convar
    flash_spectator = config.cvar('flash_spectator', 1, config_strings['Spec'])

    # Create the dead convar
    flash_dead = config.cvar('flash_dead', 1, config_strings['Dead'])


# =============================================================================
# >> FUNCTION HOOKS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, 'blind')
@EntityPreHook(EntityCondition.is_human_player, 'blind')
@EntityPreHook(EntityCondition.is_player, 'deafen')
def _block_blind_and_deafen(args):
    """Check the player's team against the flashbang's team."""
    # Is there no flashbang detonating at this time?
    if _flashbang_team is None:
        return

    # Get the player's instance
    player = make_object(Player, args[0])

    # Is player spectating?
    if player.team <= 1:

        # Allow spec flash if cvar set
        return None if flash_spectator.get_bool() else False

    # Is player dead?
    if player.dead:

        # Allow dead flash if cvar set
        return None if flash_dead.get_bool() else False

    # Is the player on a different team than the thrower?
    if player.team != _flashbang_team:
        return

    # Allow self flash
    if player.userid == _flashbang_thrower and flash_thrower.get_bool():
        return

    # Block the flash for the player
    return False


@EntityPreHook(_is_flashbang, 'detonate')
def _pre_flashbang_detonate(args):
    """Store the flashbang's thrower/team to compare against player teams."""
    global _flashbang_team, _flashbang_thrower

    # Get the weapon's instance
    weapon = make_object(Weapon, args[0])

    # Store the weapon's team
    _flashbang_team = weapon.team

    # Get the weapon's thrower
    owner = weapon.owner

    # Store the owner's userid
    if owner is not None:
        _flashbang_thrower = userid_from_index(owner.index)


@EntityPostHook(_is_flashbang, 'detonate')
def _post_flashbang_detonate(args, return_value):
    """Reset the variables so that only flashbang blinding is blocked."""
    global _flashbang_team, _flashbang_thrower
    _flashbang_team = None
    _flashbang_thrower = None
