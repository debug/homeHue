import requests
import json

ROUTER_IP = '192.168.1.2'
DEFAULT_USER = "newdeveloper"

DEBUG = False

class RouterDelegate(object):
	def __init__(self, user=DEFAULT_USER, routerIP=ROUTER_IP):
		self.__user = DEFAULT_USER
		self.__routerIP = routerIP

	def get(self, uri):
		r = requests.get("http://" + self.__routerIP + "/api/" + self.__user + "/" + uri)
		return r

	def put(self, uri, data):
		r = requests.put("http://" + self.__routerIP + "/api/" + self.__user + "/" + uri, data=data)
		return r

class Scene(RouterDelegate):
	def __init__(self):
		RouterDelegate.__init__(self, user=DEFAULT_USER, routerIP=ROUTER_IP)
#		if(isinstance(routerDelegate, RouterDelegate)):
#			self.__routerDelegate = routerDelegate
#		else:
#			raise Exception("Argument must be of kind RouterDelegate")

	def getAllLights(self):
		lights = []
#		r = requests.get("http://" + self.__routerIP + "/api/" + self.__user + "/lights")
		r = self.get("lights")
		for index, light in r.json().iteritems():
			l = Light(light['name'], index)
			lights.append(l)
		return lights

class Light(RouterDelegate):
	def __init__(self, name, id, routerDelegate=None):
		RouterDelegate.__init__(self, user=DEFAULT_USER, routerIP=ROUTER_IP)
		self.__name = name
		self.__id = id
#		self.__routerDelegate = routerDelegate
		self.__data = self.__updateState()
#		print(self.__data.keys())

	def __updateState(self):
		r = self.get("lights/" + self.__id)
		return r.json()

	def __str__(self):
		return self.__name

	@property
	def reachable(self):
		return self.__data['state']['reachable']

	def update(self):
		self.__updateState()

	@property
	def name(self):
		return self.__name

	@property
	def swVersion(self):
		return self.__data['swversion']

	@property
	def model(self):
		return self.__data['modelid']

	@property
	def lightType(self):
		return self.__data['type']

	@property
	def pointSymbol(self):
		return self.__data['pointsymbol']

	@property
	def hue(self):
		return self.__data['state']['hue']

	@property
	def on(self):
		return self.__data['state']['on']

	@property
	def brightness(self):
		return self.__data['state']['bri']

	@property
	def saturation(self):
		return self.__data['state']['sat']

	@property
	def xy(self):
		return self.__data['state']['xy']

	@property
	def temperture(self):
		return self.__data['state']['ct']

	@property
	def alert(self):
		return self.__data['state']['alert']

	@property
	def effect(self):
		return self.__data['state']['effect']

	def setOn(self):
		r = self.put("lights/{0}/state".format(self.__id), json.dumps({'on': True}))
		return r.json()[0]

	def setOff(self):
		r = self.put("lights/{0}/state".format(self.__id), json.dumps({'on': False}))
		return r.json()[0]

	def setBrightness(self, brightness):
		if(brightness < 0 or brightness > 255):
			raise Exception("Brightness value must not be less than 0 or exceed 255")
		else:
			r = self.put("lights/{0}/state".format(self.__id), json.dumps({'bri': brightness}))
			return r.json()[0]


if(__name__ == "__main__"):
	s = Scene()

	if(DEBUG):
		for light in s.getAllLights():
			print(light)
			print(light.hue)
			print(light.saturation)
			print(light.temperture)
			print(light.alert)
			print(light.effect)
			light.setOn()
			light.setBrightness(255)
