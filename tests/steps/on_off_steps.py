import time
import logging
from behave import *
from hamcrest import assert_that, equal_to, has_property, is_not

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@Step('I send the command "{state_value}" to the power supply "{psu_name}"')
def step(context, state_value, psu_name):

    psu = context.interfaces["psu"][psu_name]

    if state_value == "on":
        psu.enable.set(True)
    else:
        psu.enable.set(False)


###############################################################################
###############################################################################

@Step('the power supply "{psu}" is "{state_value}"')
def step(context, psu, state_value):

    check_value = False
    if state_value == "on":
        check_value = True

    assert_that(context.interfaces["psu"][psu].enable.get(), equal_to(check_value))
