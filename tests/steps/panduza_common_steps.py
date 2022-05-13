from behave import *
from xdocz_helpers import AttachTextLog, PathToRsc
from panduza import Core

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@Step('core aliases loaded with file "{filepath}"')
def step(context, filepath):
    Core.LoadAliases(filepath=PathToRsc(filepath))


