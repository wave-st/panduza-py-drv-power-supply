import logging
from behave import *
from fixtures.interfaces import interface_psu

###############################################################################
###############################################################################

def before_all(context):
    logging.basicConfig(level=logging.DEBUG)

###############################################################################
###############################################################################

def before_tag(context, tag):
    if tag.startswith("fixture.interface.power_supply"):
        name = tag.replace("fixture.interface.power_supply.", "")
        use_fixture(interface_psu, context, name=name)

