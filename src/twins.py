import ujson

# MQTT Topics for Azure IoT Hub Twin
SUB_TOPIC = "$iothub/twin/res/#"
RET_PUB_TOPIC = "$iothub/twin/GET/?$rid={}" #Topic for publishing to trigger twin json data from Hub
UPT_PUB_TOPIC = "$iothub/twin/PATCH/properties/reported/?$rid={}" #Topic for publishing changes in Json
DESIRED_PROP_TOPIC = "$iothub/twin/PATCH/properties/desired/#"  # Topic for desired property updates
# Payload Example
#payload = {"podaci": 50}  # Test variable

class Twins:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.request_id = 0 
        self.subscribed = 0

    def get_next_request_id(self):
        """Generate new request"""
        self.request_id += 1
        return self.request_id

    def retrieve(self, request_id=None,qos=0):
        if not self.subscribed:
            self.mqtt_client.subscribe(SUB_TOPIC,qos=qos)
            self.subscribed = 1
        #generate new request id if None
        if request_id is None:
            request_id = self.get_next_request_id()  

        topic = RET_PUB_TOPIC.format(request_id)
        self.mqtt_client.publish(topic, "",qos=qos)
        print("Sent Device Twin GET request with request ID: {}".format(self.request_id))

    def update(self, payload, request_id=None,qos=0):
        if not self.subscribed:
            self.mqtt_client.subscribe(SUB_TOPIC,qos=qos)
            self.subscribed = 1
        #generate new request id if None
        if request_id is None:
            request_id = self.get_next_request_id()  

        topic = UPT_PUB_TOPIC.format(request_id)
        self.mqtt_client.publish(topic, ujson.dumps(payload),qos=qos)
        print("Updated Device Twin with request ID: {}, payload: {}".format(request_id, payload))
    
    def subscribe_to_desired_updates(self,qos=0):
        """Subscribe to the topic for Desired Properties updates."""
        self.mqtt_client.subscribe(DESIRED_PROP_TOPIC,qos=qos)
        