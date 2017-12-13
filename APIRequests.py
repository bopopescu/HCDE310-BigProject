import config, urllib, json


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


def safeGet(url):
    try:
        return urllib.urlopen(url)
    except urllib.HTTPError, e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.URLError, e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None



# method for making a request to mapquest
# http://www.mapquestapi.com/traffic/v2/incidents?key=KEY&boundingBox=39.95,-105.25,39.52,-104.71&filters=construction,incidents
def mapquest(baseurl = 'https://www.mapquestapi.com/traffic/v2/incidents',
    key=config.mapquestKey,
    lat=47.657265,
    lon=-122.307208,
    params={}
    ):
    # boundingBox = 39.95, -105.25, 39.52, -104.71
    params['boundingBox'] = str(lat+.05) + ',' + str(lon-.05) + ',' + str(lat-.05) + ',' + str(lon+.05)
    params['key'] = key
    url = baseurl + "?" + urllib.urlencode(params)
    info = json.loads(safeGet(url).read())
    return info


# testmq = json.loads(mapquest().read())
# print(pretty(testmq))


# method for making a request to bing
# http://dev.virtualearth.net/REST/v1/Traffic/Incidents/mapArea/includeLocationCodes?severity=severity1,severity2,severityn&type=type1,type2,typen&key=BingMapsKey
def bing(baseurl = 'https://dev.virtualearth.net/REST/v1/Traffic/Incidents/',
    lat=47.657265,
    lon=-122.307208,
    params = {}
    ):

    mapArea = str(lat-.05) + ',' + str(lon-.05) + ',' + str(lat+.05) + ',' + str(lon+.05)
    params['t'] = '1,2,3,4,5,6,7,8,9,10,11'
    params['key'] = config.bingKey
    params['includeLocationCodes'] = 'true'
    url = baseurl + mapArea + "?" + urllib.urlencode(params)
    info = json.loads(safeGet(url).read())
    return info


# testbing = json.loads(bing().read())
# print(pretty(testbing))
#
# for report in testbing['resourceSets'][0]['resources']:
#     print(str(report['point']['coordinates'][0]) + ', ' + str(report['point']['coordinates'][1]))


# method for making a request to wsdot
def wsdot(baseurl = '',
    params = {}
    ):
    url = baseurl + "?" + urllib.urlencode(params)
    return safeGet(url)


# testwsdot = json.loads(wsdot().read())
# print(pretty(testwsdot))


# method for creating our google map
def googlemap():
    print()

# method for making a request to weather underground
# http://api.wunderground.com/api/Your_Key/conditions/q/lat,lon.json

def wunderground(baseurl = 'https://api.wunderground.com/api/',
    lat=47.657265,
    lon=-122.307208,
    method = 'conditions',
    api_key = config.weatherKey,
    format = 'json'
    ):
    url = baseurl + api_key + '/' + method + '/q/' + str(lat) + ',' + str(lon) + '.' + format
    info = json.loads(safeGet(url).read())
    return info


# testwu = json.loads(wunderground().read())
# print(pretty(testwu))


# bing data refinement
def bRefine(info):
    data = {}
    for incident in info['resourceSets'][0]['resources']:
        list = {}
        list['startCoordinates'] = (str(incident['point']['coordinates'][0]) + ',' + str(incident['point']['coordinates'][1]))
        list['endCoordinates'] = (str(incident['toPoint']['coordinates'][0]) + ',' + str(incident['toPoint']['coordinates'][1]))
        # Severity scale 0-4
        list['severity'] = (incident['severity'])
        # road closed?
        list['closed'] = (incident['roadClosed'])
        data[incident['description']] = list
    return data


# mapquest data refinement
# severity 0-4
# type key; 1 = Construction, 2 = Event, 3 = Congestion/Flow, 4 = Incident/accident


def mRefine(info):
    data = {}
    for incident in info['incidents']:
        list = {}
        # lat,lon of incident
        list['coordinates'] = str(incident['lat']) + ',' + str(incident['lng'])
        # Severity scale 0-4
        list['severity'] = incident['severity']
        # impacting key is whether it impacts traffic
        list['impact'] = incident['impacting']
        data[incident['fullDesc']] = list
    return data


# average data of severity on 0-4 scale, average qualitative data
def averageData(info):
    severityAvg = 0
    incidentAvg = ''
    avg = {}
    severityAvg = bRefine(list['severity']) + mRefine(list['severity'])
    incidentAvg = bRefine(list['closed']) + mRefine(list['impact'])
    avg['severityAvg'] = severityAvg
    avg['incidentAvg'] = incidentAvg
    return avg

# weather data refinement
def wRefine(info):
    data = {}
    list = {}
    list['coordinates'] = str(info['current_observation']['observation_location']['latitude']) +\
                          ',' + str(info['current_observation']['observation_location']['longitude'])
    list['temp'] = info['current_observation']['temperature_string']
    list['feelslike'] = info['current_observation']['feelslike_string']
    list['weather'] = info['current_observation']['weather']
    list['wind'] = info['current_observation']['wind_string']
    data[info['current_observation']['observation_location']['full']] = list
    return data


# bing print method
def dataPrint(information):
    s = ""
    if len(information) == 0:
        return("This location has no traffic incidents or data.")
    else:
        for info in information:
            s += info+'\n'
            for value in information[info]:
                s+= ('\t%s'%(value) + ' = %s\n'%information[info][value])
    return(s)






class UserCall(object):
    def __init__(self, lat=47.657265, lon=-122.307208):
        self.bing = bing(lat=lat,lon=lon)
        self.mapquest = mapquest(lat=lat, lon=lon)
        self.weather = wunderground(lat=lat, lon=lon)

    def __str__(self):
        return "test text"


if __name__ == '__main__':
    latitude = input('Please enter a latitude: ')
    print("latitude = 47.657265")
    longitude = input('Please enter a longitude: ')
    print('longitude = 122.307208')
    print()
    userinput = UserCall(lat=float(latitude), lon=float(longitude))
    print(userinput)


# print('--__BING__--')
# print('...testing bing refine...')
# print()
# dataPrint(bRefine(userinput.bing))
# print()
#
# print('--__MAPQUEST__--')
# print('...testing mapquest refine...')
# print()
# dataPrint(mRefine(userinput.mapquest))
# print()
#
# print('--__WEATHER__--')
# print('...testing weather refine...')
# print()
# dataPrint(wRefine(userinput.weather))
# print()