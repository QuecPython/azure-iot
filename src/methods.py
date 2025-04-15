import ujson
import log

class Method(object):
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.logging = log.getLogger("Method")
        
    def init_direct_method_handler(self, method_handler): 
        try:
            self.mqtt_client.set_callback("$iothub/methods/POST/#", method_handler)
            self.mqtt_client.subscribe("$iothub/methods/POST/#")
        except:
            self.logging.error("Initialization of direct method handled error")

    def send_method_response(self, status, message, request_id):
        response_topic = "$iothub/methods/res/{}/?$rid={}".format(status, request_id)
        self.mqtt_client.publish(response_topic, ujson.dumps({"result": message}))