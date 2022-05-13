from behave import *
from xdocz_helpers import AttachTextLog, PathToRsc
from panduza import Core

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@Step('power supply interface "{interface_name}" initialized with alias "{interface_alias}"')
def step(context, interface_name, interface_alias):
    context.interfaces["psu"][interface_name].init(alias=interface_alias)

