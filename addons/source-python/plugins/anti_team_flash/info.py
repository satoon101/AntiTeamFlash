# ../anti_team_flash/info.py

"""Provides/stores information about the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.public import PublicConVar
#   Plugins
from plugins.info import PluginInfo


# =============================================================================
# >> PLUGIN INFO
# =============================================================================
info = PluginInfo()
info.name = 'Anti Team Flash'
info.author = 'Satoon101'
info.version = '1.2'
info.basename = 'anti_team_flash'
info.variable = info.basename + '_version'
info.url = 'http://forums.sourcepython.com/showthread.php?895'
info.convar = PublicConVar(info.variable, info.version, info.name + ' Version')
