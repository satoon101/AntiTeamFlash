# ../anti_team_flash/anti_team_flash.py

"""Stops players from being flashed by teammates."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from entities.hooks import EntityCondition
from entities.hooks import EntityPostHook
from entities.hooks import EntityPreHook
from memory import make_object
from players.entity import Player
from players.helpers import userid_from_index
from weapons.entity import Weapon

# Plugin
from .config import flash_dead, flash_spectator, flash_thrower


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


@EntityPreHook(
    EntityCondition.equals_entity_classname('flashbang_projectile'),
    'detonate'
)
def _pre_flashbang_detonate(stack_data):
    _flash_manager.pre_detonate(stack_data)


@EntityPostHook(
    EntityCondition.equals_entity_classname('flashbang_projectile'),
    'detonate'
)
def _post_flashbang_detonate(stack_data, return_value):
    _flash_manager.post_detonate()
