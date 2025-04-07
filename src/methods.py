import ujson

class Method(object):
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.mqtt_client.set_callback("$iothub/methods/POST/#",self.handle_method)

    def handle_method(self, method_name, msg):
        if method_name == "turn_on_light":
            # Uključi svetlo
            print("Svetlo uključeno!")
            self.send_response(200, "Svetlo je uključeno")
        else:
            self.send_response(404, "Metoda nije pronađena")

    def send_method_response(self, status, message):
        response_topic = "$iothub/methods/res/{}/?$rid={}".format(status, request_id)
        self.client_id.publish(response_topic, ujson.dumps({"result": message}))