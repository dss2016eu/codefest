from settings.constants import SettingsGenerator
from handlers.db_handler import DBManagerFactory
from handlers.db_handler import DB_NAME
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask, render_template, request
from markers import get_markers

app = Flask(__name__, template_folder=".")
GoogleMaps(app)

@app.route("/", methods=['GET', 'POST'])
def parse_request():
    # Retrieve app settings
    settings = SettingsGenerator().get_settings()
    # Construct database manager
    db_manager = DBManagerFactory(settings, DB_NAME).get_manager()
    app.config['GOOGLEMAPS_KEY'] = settings.get('GOOGLE_MAPS', 'api_key')
    # Configure map
    mymap = Map(
        identifier="mymap",
        lat=49.863738,
        lng=14.38623,
        # Get requested markers
        markers=get_markers(request, db_manager),
        style="height:600px;width:800px;margin:0;",
        zoom=4
    )
    # Render map
    return render_template('index.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True)