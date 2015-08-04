# ../anti_team_flash/anti_team_flash.py

"""."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Entities
from entities.hooks import EntityPostHook
from entities.hooks import EntityPreHook
#   Memory
from memory import make_object
#   Players
from players.entity import PlayerEntity
#   Weapons
from weapons.entity import WeaponEntity


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create the team variable to check against later
_flashbang_team = None


# =============================================================================
# >> FUNCTION HOOKS
# =============================================================================
@EntityPreHook('CCSBot', 'blind')
def _pre_bot_blind(args):
    """Check the bot's team to determine if blind needs blocked."""
    return _block_team_flash(args)


@EntityPreHook('CCSPlayer', 'blind')
def _pre_player_blind(args):
    """Check the player's team to determine if blind needs blocked."""
    return _block_team_flash(args)


@EntityPreHook('CCSPlayer', 'deafen')
def _pre_player_deafen(args):
    """Check the player's team to determine if deafen needs blocked."""
    return _block_team_flash(args)


@EntityPreHook('CFlashbangProjectile', 'detonate')
def _pre_flashbang_detonate(args):
    """Store the flashbang's team to compare against player teams."""
    global _flashbang_team
    weapon = make_object(WeaponEntity, args[0])
    _flashbang_team = weapon.team


@EntityPostHook('CFlashbangProjectile', 'detonate')
def _post_detonate(args, return_value):
    """Reset the team variable so that only flashbang blinding is blocked."""
    global _flashbang_team
    _flashbang_team = None


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

    # Block the function if the teams match
    if player.team == _flashbang_team:
        return False
