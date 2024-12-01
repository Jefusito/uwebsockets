# MicroPython WebSocket Client without USSL

This repository contains a small modification of the WebSocket client for MicroPython, based on [uwebsockets](https://github.com/danni/uwebsockets). 

## Features

- Supports WebSocket (`ws://`) and secure WebSocket (`wss://`) connections in trusted networks.
- Optimized implementation for MicroPython without dependencies like `logging` or `ussl`.

⚠️ **Warning:** `wss://` connections in this implementation do not use SSL/TLS encryption, making them insecure for public networks.


## Example Code:


```python
from uwebsockets.client import connect

# Connect to the WebSocket server
ws = connect("ws://host:port/path")  # Replace with your WebSocket URL

# Send a message
ws.send("Hello from MicroPython!")

# Receive a response
response = ws.recv()
print("Received response:", response)

# Close the connection
ws.close()

```

## Notes
- Security: This WebSocket client does not implement encryption for wss:// connections. Using a secure proxy is recommended if TLS encryption is needed.
- Compatibility: Tested on MicroPython for Raspberry Pi Pico W, ESP32, and ESP8266.