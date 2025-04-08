'''
KEY_PATH = env.get("PRIVATE_KEY_PATH")
CERT_PATH = env.get("CERTIFICATE_PATH")
PRIMARY_DEVICE_KEY = env.get("PRIMARY_DEVICE_KEY")
'''
#arguments for x.509 certificate
PRIVATE_KEY = None
CERT = None

#taken from primary or secondary key, used for SAS token authorization
SHARED_ACCESS_KEY = None

#password can be SAS token that you created in Azure IoT Explorer
PASSWORD = None

