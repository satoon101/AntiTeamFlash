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
# >> CLASSES
# =============================================================================
class _FlashManager(object):
    flashbang_team = None
    flashbang_thrower = None

    def pre_detonate(self, stack_data):
        """Store the flashbang's thrower/team."""
        # Store the team
        weapon = make_object(Weapon, stack_data[0])
        self.flashbang_team = weapon.team

        # Store the owner's userid
        owner = weapon.owner
        if owner is not None:
            self.flashbang_thrower = userid_from_index(owner.index)

    def post_detonate(self):
        """Reset the variables so that only flashbang blinding is blocked."""
        self.flashbang_team = None
        self.flashbang_thrower = None

    def should_block_blind_and_deafen(self, stack_data):
        """Block blinding and deafening if player should not be flashed."""
        # Is there no flashbang detonating at this time?
        if self.flashbang_team is None:
            return

        # Block for spectating player?
        player = make_object(Player, stack_data[0])
        if player.team <= 1:
            return None if flash_spectator.get_bool() else False

        # Block for dead player?
        if player.dead:
            return None if flash_dead.get_bool() else False

        # Don't block for enemy player
        if player.team != self.flashbang_team:
            return

        # Block for self flash?
        if (
            player.userid == self.flashbang_thrower and
            flash_thrower.get_bool()
        ):
            return

        # Block the flash for the player
        return False

_flash_manager = _FlashManager()


# =============================================================================
# >> FUNCTION HOOKS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, 'blind')
@EntityPreHook(EntityCondition.is_human_player, 'blind')
@EntityPreHook(EntityCondition.is_player, 'deafen')
def _block_blind_and_deafen(stack_data):
    return _flash_manager.should_block_blind_and_deafen(stack_data)


@EntityPreHook(_is_flashbang, 'detonate')
def _pre_flashbang_detonate(stack_data):
    _flash_manager.pre_detonate(stack_data)


@EntityPostHook(_is_flashbang, 'detonate')
def _post_flashbang_detonate(stack_data, return_value):
    _flash_manager.post_detonate()
