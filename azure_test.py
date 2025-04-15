import usr.azure as azure
import modem
import ujson
from usr.config import CERT,PRIVATE_KEY,SHARED_ACCESS_KEY, PASSWORD


# device name
client_id = 'device123'
# server address
server = 'qp-hub.azure-devices.net'
# port MQTT
port = 8883

username = '{}/{}/?api-version=2021-04-12'.format(server, client_id)

uri = "{}/devices/{}".format(server, client_id)
SharedAccessKey = SHARED_ACCESS_KEY

def event_callback(data):
    pass

# create azure obj
azure_obj = azure.Azure(client_id, server, port, keep_alive=60, user=username, password=PASSWORD, ssl=True, ssl_params={"cert": 
CERT, "key": PRIVATE_KEY})
print("create azure obj")

#generate token 
token = azure_obj.generate_sas_token(uri, SharedAccessKey, None)
azure_obj.mqtt_client.password = token

# connect mqtt server
print("azure connect start")
azure_obj.connect()
print("azure connect end")


azure_obj.start()