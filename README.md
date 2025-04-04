#  IoT Device SDK for Azure with QuecPython

## Project Description

This solution enables establishing an MQTT connection with **Azure IoT Hub** using the `azure.py` library written for **QuecPython**.

One of the main challenges I faced was generating the **SAS token** and dealing with the absence of certain Python features, since **QuecPython** is a limited environment compared to standard Python. However, thanks to the solid support and flexibility offered by QuecPython, I was able to overcome these limitations and implement a reliable communication layer with Azure IoT Hub.

This project serves as a lightweight SDK for IoT devices based on Quectel modules, allowing integration with Azure’s IoT ecosystem even in constrained environments.

##  How to Install and Run the Project

To get started with this project, you should first clone the Repository:

Clone the project to your local machine using:

```bash
git clone https://github.com/QuecPython/azure-iot.git
```
Then set up the QuecPython development environment.
Follow the official QuecPython Getting Started Guide to set up all necessary tools:
https://python.quectel.com/doc/Getting_started/en/index.html

This guide walks you through:

Installing the required drivers for Quectel modules

Downloading and installing the IDE (QPYcom or QPYcom-IDE)

Flashing the latest QuecPython firmware

Setting up the development environment and connecting your module via USB

After completing the steps, you will be ready to run the example code and test MQTT connectivity to Azure IoT Hub.

## How to Use the Project

To use this program, you must first have a Microsoft Azure account and register a device on your IoT Hub.

You can follow the steps in the official Azure guide here:  
**#TODO Add link to Azure IoT Hub device creation guide**

Azure supports several authentication methods for connecting devices.  
In this project, we demonstrate two commonly used methods:

1. **SAS Token Authentication**
2. **x.509 Certificate Authentication**

---

### Example: x.509 Certificate Authentication

```python
import usr.azure as azure
import modem
import ujson
from usr.config import CERT, PRIVATE_KEY, SHARED_ACCESS_KEY, PASSWORD

client_id = 'device_qp'
server = 'qp-hub.azure-devices.net'
port = 8883
username = None

def event_callback(data):
    pass

# create Azure object
azure_obj = azure.Azure(client_id, server, port, keep_alive=60, user=username, password=PASSWORD, ssl=True, ssl_params={"cert": CERT, "key": PRIVATE_KEY})
print("create azure obj")

# connect to MQTT server
print("azure connect start")
azure_obj.connect()
print("azure connect end")

azure_obj.start()
```
### Example: SAS Token Authentication

```python
import usr.azure as azure
import modem
import ujson
from usr.config import CERT, PRIVATE_KEY, SHARED_ACCESS_KEY, PASSWORD

client_id = 'device_qp'
server = 'qp-hub.azure-devices.net'
port = 8883
username = '{}/{}/?api-version=2021-04-12'.format(server, client_id)

uri = "{}/devices/{}".format(server, client_id)
SharedAccessKey = SHARED_ACCESS_KEY

def event_callback(data):
    pass

# create Azure object
azure_obj = azure.Azure(client_id, server, port, keep_alive=60, user=username, password=PASSWORD, ssl=True, ssl_params={"cert": CERT, "key": PRIVATE_KEY})
print("create azure obj")

# generate SAS token
token = azure_obj.generate_sas_token(uri, SharedAccessKey, None)
azure_obj.mqtt_client.password = token

# connect to MQTT server
print("azure connect start")
azure_obj.connect()
print("azure connect end")

azure_obj.start()
```
---
### Configuration: `usr/config.py`

Before running the examples, make sure to properly set the variables inside your `usr/config.py` file. This file stores all credentials and paths required for authentication.

```python

# Arguments for x.509 certificate authentication
PRIVATE_KEY = None     # Private key - content from private_key.key file
CERT = None            # Certificate - content from .pem file 

# Taken from primary or secondary key, used for SAS token generation
SHARED_ACCESS_KEY = None

# Used as password in MQTT client – can be a SAS token created in Azure IoT Explorer
PASSWORD = None
```
How to insert certificate or key content:
```python
PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
    key content 
-----END PRIVATE KEY-----
"""
```