from usr.mqtt_client import MQTTClientWrapper
from usr.twins import Twins
from usr.methods import Method
import ujson
import log
import math
import utime
import usr.sastoken as sas

from base64 import b64encode, b64decode
from hashlib import sha256
from hmac import HMAC

PUB_TOPIC = "devices/{device-id}/messages/events/"  # Topic for publishing to IoT Hub
SUB_TOPIC = "devices/{device-id}/messages/devicebound/#" #Topic for recieving from IoT Hub


class Azure(object):
    """
    Azure IoT Core client
    """
    def __init__(self, client_id, server, port, keep_alive=60, user=None, password=None, ssl=False, ssl_params=None):
        self.client_id = client_id                                                                                     
        self.mqtt_client = MQTTClientWrapper(client_id, server, port, keep_alive, user, password, ssl, ssl_params)    
        self.twins_manager = Twins(self.mqtt_client)
        self.logging = log.getLogger("Azure")
        self.direct_method = Method(self.mqtt_client)

    # Used for connecting to Azure IoT Core (server)
    def connect(self):
        self.mqtt_client.connect()

    # Used for disconnecting from server
    def disconnect(self):
        self.mqtt_client.disconnect()

    # Used for subscribing to MQTT topic
    def subscribe(self, topic,qos=0):
        self.mqtt_client.subscribe(topic,qos=qos)

    # Used for publishing to MQTT topic
    def publish(self, topic, payload,qos=0):
        self.mqtt_client.publish(topic, payload,qos=qos)

    # Set callback method
    def set_callback(self, topic_name, callback):
        self.mqtt_client.set_callback(topic_name,callback)

    def loop(self):
        self.mqtt_client.loop()

    def start(self):
        self.mqtt_client.start()

    def retrieve_twin(self, request_id=None, qos=0):
        self.twins_manager.retrieve(request_id,qos=qos)
    
    def update_twin(self, payload, request_id=None,qos=0):
        self.twins_manager.update(payload,request_id,qos=qos)
    
    def subscribe_to_desired_updates(self,qos=0):
        self.twins_manager.subscribe_to_desired_updates(qos=qos)

    def init_direct_method_handler(self, method_handler): 
        self.direct_method.init_direct_method_handler(method_handler)

    def send_method_response(self, status, message, request_id):
        self.direct_method.send_method_response(status,message,request_id)

    def generate_sas_token(self, uri, key, policy_name, expiry=3600):
        token = sas.generate_sas_token(uri,key,policy_name,expiry)
        return token
    
    

