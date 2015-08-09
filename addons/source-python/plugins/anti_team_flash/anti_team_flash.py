# ../anti_team_flash/anti_team_flash.py

"""Stops players from being flashed by teammates."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Config
from config.manager import ConfigManager
#   Cvars
from cvars.flags import ConVarFlags
#   Entities
from entities.hooks import EntityCondition
from entities.hooks import EntityPostHook
from entities.hooks import EntityPreHook
#   Memory
from memory import make_object
#   Players
from players.entity import PlayerEntity
from players.helpers import userid_from_index
#   Translations
from translations.strings import LangStrings
#   Weapons
from weapons.entity import WeaponEntity

# Script Imports
from anti_team_flash.info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create the team variable to check against later
_flashbang_team = None

# Create the thrower variable to check against later
_flashbang_thrower = None

# Get the config strings to use
config_strings = LangStrings(info.basename)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the config file
with ConfigManager(info.basename, 'atf_') as config:

    # Create the thrower convar
    flash_thrower = config.cvar(
        'flash_thrower', 0, ConVarFlags.NONE, config_strings['Thrower'])


# =============================================================================
# >> FUNCTION HOOKS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, 'blind')
def _pre_bot_blind(args):
    """Check the bot's team to determine if blind needs blocked."""
    return _block_team_flash(args)


@EntityPreHook(EntityCondition.is_human_player, 'blind')
def _pre_player_blind(args):
    """Check the player's team to determine if blind needs blocked."""
    return _block_team_flash(args)


@EntityPreHook(EntityCondition.is_player, 'deafen')
def _pre_player_deafen(args):
    """Check the player's team to determine if deafen needs blocked."""
    return _block_team_flash(args)


@EntityPreHook(
        EntityCondition.equals_entity_classname('flashbang_projectile'),
        'detonate')
def _pre_flashbang_detonate(args):
    """Store the flashbang's thrower/team to compare against player teams."""
    global _flashbang_team, _flashbang_thrower

    # Get the weapon's instance
    weapon = make_object(WeaponEntity, args[0])

    # Store the weapon's team
    _flashbang_team = weapon.team

    # Get the weapon's thrower
    owner = weapon.current_owner

    # Store the owner's userid
    if owner is not None:
        _flashbang_thrower = userid_from_index(owner.index)


@EntityPostHook(
        EntityCondition.equals_entity_classname('flashbang_projectile'),
        'detonate')
def _post_detonate(args, return_value):
    """Reset the variables so that only flashbang blinding is blocked."""
    global _flashbang_team, _flashbang_thrower
    _flashbang_team = None
    _flashbang_thrower = None


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _block_team_flash(args):
    """Check the player's team against the flashbang's team."""
    # Is there no flashbang detonating at this time?
    if _flashbang_team is None:
        return

    # Get the player's instance
    player = make_object(PlayerEntity, args[0])

    # Is the player on a different team than the thrower?
    if player.team != _flashbang_team:
        return

    # Allow self flash
    if player.userid == _flashbang_thrower and flash_thrower.get_int():
        return

    # Block the flash for the player
    return False
