Feature: On/Off Management
    As a user, I want to be able to enable or disable the power supply

    @fixture.interface.power_supply.test
    Scenario: Try to turn off en on again
    
        Given core aliases loaded with file "psu_alias.json"
        And  power supply interface "test" initialized with alias "psu_test"
        When I send the command "on" to the power supply "test"
        Then the power supply "test" is "on"
        When I send the command "off" to the power supply "test"
        Then the power supply "test" is "off"


