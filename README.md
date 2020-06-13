# A Python3 wrapper for LD686-compatible LED controllers.

No longer developing this, as [flux led](https://github.com/beville/flux_led) makes this obsolete.

## Reverse-Engineered Protocol of LD686

###  <a name="checksum"></a>Checksum
The Checksum is the first byte of the sum all prior bytes (including the Delimiter)

```python
    checksum = 0
    for byte in data_bytes:
        checksum += byte
    checksum = checksum & 0xFF
```

### Power Commands

The Message to set the Power is composed of the following bytes
 1. `0x71` "Set Power"
 2. "Power State" (If given an unknown state, the power state stays unchanged, but the response is sent. Useful for querying the state)
    * `0x22` "ON"
    * `0x23` "ON"
    * `0x24` "OFF"
 3. `0x0f` "Delimiter"
 4. [Checksum](#checksum)

The LD686 responds with:
 1. `0x0f` (But this byte is literally the third byte of the request as seen [here](#power-remarks))
 2. `0x71` "Power State:"
 3. "Power State"
    * `0x23` "ON"
    * `0x24` "OFF"
 4. [Checksum](#checksum)

#### <a name="power-remarks"></a>Remarks
I believe that this is unintended behaviour but, it's possible to send a request that leaves out the second byte to get the current Power state in the response without setting the power state. 
```
0x71 0x0f 0x80
```
Where `0x80` is the checksum.

The following response looks like this:
```
0x80 0x71 [POWER STATE]
```

### Color Commands

The Message to set the Color is composed of the following bytes
1. `0x31` "Set Color"
2. Red
3. Green
4. Blue
5. White1
6. White2
7. `0x00` "Delimiter?"
8. Strange Byte
   * Anything except `0x00`
9. [Checksum](checksum)


### Query Commands

The query command is composed of the following bytes:
1. `0x81`
2. `0x8a`
3. `0x8b`

The response 

### Program Commands

### Programs
```
    seven_color_cross_fade =   0x25
    red_gradual_change =       0x26
    green_gradual_change =     0x27
    blue_gradual_change =      0x28
    yellow_gradual_change =    0x29
    cyan_gradual_change =      0x2a
    purple_gradual_change =    0x2b
    white_gradual_change =     0x2c
    red_green_cross_fade =     0x2d
    red_blue_cross_fade =      0x2e
    green_blue_cross_fade =    0x2f
    seven_color_strobe_flash = 0x30
    red_strobe_flash =         0x31
    green_strobe_flash =       0x32
    blue_strobe_flash =        0x33
    yellow_strobe_flash =      0x34
    cyan_strobe_flash =        0x35
    purple_strobe_flash =      0x36
    white_strobe_flash =       0x37
    seven_color_jumping =      0x38
```

## Resources
https://github.com/beville/flux_led/blob/b09c9b718d35c7c3355da53904d5e45e2e42145c/flux_led/__main__.py#L656