# Panduza Python Class Power Supply




## Power supply hm7044

```json
"interfaces": [
    {
        "name": "my_power_supply",
        "driver": "psu_hm7044",
        "settings": {
            "serial_port" : "/dev/ttyACM0",
            "channel" : 1                       // [1,2,3,4]
        }
    }
]
```


