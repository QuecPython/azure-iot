from umqtt import MQTTClient
import ujson
import utime as time
import log

class MQTTClientWrapper:
    def __init__(self, client_id, server, port, keep_alive=60, user=None, password=None, ssl=False, ssl_params=None):
        self.client_id = client_id                  
        self.server = server                        
        self.port = port
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.keep_alive = keep_alive
        self.user = user
        self.password = password
        self.client = None
        self.connected = False
        self.callbacks = {}                     
        self.logging = log.getLogger("MQTT")
        
        
    def _connect(self):
        try:
            self.client = MQTTClient(self.client_id,
                                    self.server,
                                    port=self.port,
                                    keepalive=self.keep_alive,
                                    user=self.user,
                                    password=self.password,
                                    ssl=self.ssl,
                                    ssl_params=self.ssl_params)
            self.client.connect()
            self.connected = True
            self.client.set_callback(self._handle_message)
            self.logging.info("Connected to MQTT Broker")
            return True
        except Exception as e:
            self.logging.error("Failed to connect to MQTT Broker: %s", e)
            return False

    def set_callback(self, topic_name, callback):
        self.callbacks[topic_name] = callback

    # Default callback called for every contact from server. 
    def _handle_message(self, topic, msg):
        self.logging.info("Message received on {}: {}".format(topic, msg))
        try:
            msg_json = ujson.loads(msg)
            top = topic.decode()
            if top.startswith("$iothub/methods/POST/"):
                top = "$iothub/methods/POST/#"
            if top in self.callbacks:
                if top.startswith("$iothub/methods/POST/"):
                    method_name = topic.decode().split('/')[3]
                    request_id = topic.decode().split('?$rid=')[1]
                    self.callbacks[top](method_name, msg_json, request_id)
                self.callbacks[top](msg_json)                                                   # Calling the matching callback from a list
        except ValueError as e:
            self.logging.error("Failed to parse JSON message on topic {}: {}".format(topic, e))

    def connect(self):
        if not self.check_connection():
            self._connect()

    def check_connection(self):
        return self.connected

    def disconnect(self):
        try:
            if self.client:
                self.client.disconnect()
                self.client = None
                self.connected = False
                self.logging.info("Disconnected from MQTT Broker")
                return True
        except Exception as e:
            self.logging.error("Failed to disconnect from MQTT Broker: %s", e)
            return False

    def subscribe(self, topic, qos=0):
        try:
            if self.client:
                self.client.subscribe(topic,qos=qos)
                self.logging.info("Subscribed to topic: %s", topic)
                return True
        except Exception as e:
            self.logging.error("Failed to subscribe to topic %s: %s", topic, e)
            return False

    def publish(self, topic, payload, qos=0):
        try:
            if self.client:
                self.client.publish(topic, payload,qos=qos)
                self.logging.info("Published to topic: %s", topic)
        except Exception as e:
            self.logging.error("Failed to publish message to topic %s: %s", topic, e)

    def loop(self):
        try:
            while True:
                if self.client:
                    self.client.wait_msg()
                else:
                    time.sleep_ms(100)
        except Exception as e:
            self.logging.error("Error in MQTT loop: %s", e)

    def start(self):
        import _thread
        _thread.start_new_thread(self.loop, ())