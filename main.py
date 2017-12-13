import config, os, logging, APIRequests, geocoder, jinja2
from flask import Flask


app = Flask(__name__)


#MapUrl with traffic?
g = geocoder.ip('me')
print(g.latlng)
userinput = APIRequests.UserCall(lat=float(g.lat), lon=float(g.lng))
googleMapUrl = "https://www.google.com/maps/embed/v1/view?key=%s&center=%s,%s&zoom=12"%(config.googleMapKey,g.lat,g.lng)
#Weather
UGWeather = APIRequests.wRefine(userinput.weather)


#Incidents
bing = APIRequests.dataPrint(APIRequests.bRefine(userinput.bing))
mapquest = APIRequests.mRefine(userinput.mapquest)

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

tvals = {'location':g.city,'lat': g.lat,'lng':g.lng,'mapURL': googleMapUrl, 'bing' : bing, 'mapquest' : mapquest, 'weather' : UGWeather}
for a in tvals:
    print(tvals[a])
f = open("output.html", 'w')
template = JINJA_ENVIRONMENT.get_template('indexClean.html')
f.write(template.render(tvals))
f.close()


@app.route('/')
def index():
    index = JINJA_ENVIRONMENT.get_template('indexClean.html').render(tvals)
    return index


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# print(testusercall)
