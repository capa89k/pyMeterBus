Meter-Bus for Python
====================

About
-----

[M-Bus](http://www.m-bus.com/) (Meter-Bus) is a European standard (EN 13757-2 physical and link layer, EN 13757-3 application layer) for the remote reading of gas or electricity meters. M-Bus is also usable for other types of consumption meters. The M-Bus interface is made for communication on two wires, making it very cost effective.

This repository is a fork that aims to port the code on  micropython device (currently only tested againt a LoPy4).

Based on the original work of Mikael Ganehag Brorsson.

**WARNING: this repo is working in progress, don't use it!**

Known Issues
------------
* Missing: Fixed data structure parsing.
* Missing: Encoding to M-Bus frames.
* Missing: Slave configuration.
* Missing: Extended VIF codes.


What works
----------

* Querying a M-Bus device over serial.
* Parsing of a complete telegram.
* Parsing of just the *Used Data* segment.
* Generation of a basic JSON structure from the telegram/user-data/records.


Basic API documentation
-----------------------

#### meterbus.load(data)
* data[str]: M-Bus frame data

Returns an object of either type *WTelegramSndNr, TelegramACK, TelegramShort, TelegramControl* or *TelegramLong*. If an error occurs, it will raise a *MBusFrameDecodeError*.

#### meterbus.debug(state)
* state[bool]: set the global debug state

Produces debug messages to stdout.

#### meterbus.send_ping_frame(ser, address)
* ser[pySerial connection]: an open pySerial object
* address: The target primary address

Sends a PING frame to *address* over the serial connection *ser*.

#### meterbus.recv_frame(ser, length)
* ser[pySerial connection]: an open pySerial object
* length: The minimum length of the reply. An ACK frame is one (1) byte.

Reads an entire frame and returns the unparsed data.

#### meterbus.send_request_frame_multi(ser, address, req)
* ser[pySerial connection]: an open pySerial object
* address: The target primary address

If *req* is None, build a new *request* frame using *address* and send it.

#### meterbus.send_select_frame(ser, secondary_address)
* ser[pySerial connection]: an open pySerial object
* secondary_address[str]: A target using secondary address format

Sends a select frame with the supplied secondary address.

#### meterbus.XXX
More to come...


Code examples
-------------

### Decode the value of a single record (record 3)
```python
import meterbus

data = "\x68\x6A\x6A\x68\x08\x01\x72\x43\x53\x93\x07\x65" \
       "\x32\x10\x04\xCA\x00\x00\x00\x0C\x05\x14\x00\x00" \
       "\x00\x0C\x13\x13\x20\x00\x00\x0B\x22\x01\x24\x03" \
       "\x04\x6D\x12\x0B\xD3\x12\x32\x6C\x00\x00\x0C\x78" \
       "\x43\x53\x93\x07\x06\xFD\x0C\xF2\x03\x01\x00\xF6" \
       "\x01\x0D\xFD\x0B\x05\x31\x32\x4D\x46\x57\x01\xFD" \
       "\x0E\x00\x4C\x05\x14\x00\x00\x00\x4C\x13\x13\x20" \
       "\x00\x00\x42\x6C\xBF\x1C\x0F\x37\xFD\x17\x00\x00" \
       "\x00\x00\x00\x00\x00\x00\x02\x7A\x25\x00\x02\x78" \
       "\x25\x00\x3A\x16"

telegram = meterbus.load(data)
print telegram.records[3].parsed_value
```

```shell
~$ 2014-02-19T11:18
```

### Request a frame over Serial and dump it in JSON format
```python
import serial
import meterbus

address = 254

with serial.Serial('/dev/ttyACM0', 2400, 8, 'E', 1, 0.5) as ser:
  meterbus.send_ping_frame(ser, address)
  frame = meterbus.load(meterbus.recv_frame(ser, 1))
  assert isinstance(frame, meterbus.TelegramACK)

  meterbus.send_request_frame(ser, address)
  frame = meterbus.load(meterbus.recv_frame(ser, meterbus.FRAME_DATA_LENGTH))
  assert isinstance(frame, meterbus.TelegramLong)

  print(frame.to_JSON())
```

M-Bus Packet Format
-------------------

| Single Character | Short Frame | Control Frame | Long Frame             |
|------------------|-------------|---------------|------------------------|
| E5h              | Start 10h   | Start 68h     | Start 68h              |
|                  | C Field     | L Field = 3   | L Field                |
|                  | A Field     | L Field = 3   | L Field                |
|                  | Check Sum   | Start 68h     | Start 68h              |
|                  | Stop 16h    | C Field       | C Field                |
|                  |             | A Field       | A Field                |
|                  |             | CI Field      | CI Field               |
|                  |             | Check Sum     | User Data (0-252 Byte) |
|                  |             | Stop 16h      | Check Sum              |
|                  |             |               | Stop 16h               |



License
-------
Please see the [LICENSE](LICENSE) file
