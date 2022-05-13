from behave import fixture
from panduza import PowerSupply

@fixture
def interface_psu(context, name):
    # -- SETUP-FIXTURE PART:
    if "interfaces" not in context:
        context.interfaces = dict()
    if "psu" not in context.interfaces:
        context.interfaces["psu"] = dict()
    context.interfaces["psu"][name] = PowerSupply()

    # -- READY FOR THE STEP --
    yield context.interfaces["psu"][name]

    # -- CLEANUP-FIXTURE PART:

