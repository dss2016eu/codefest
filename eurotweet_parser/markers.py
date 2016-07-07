import re
from settings.constants import date_intervals, tag_selections

coordinates_regex = "[-]?\d+\.\d+"
delimiter = ";"

def get_markers(request, db_manager):
    markers= []
    if request.method == "POST":
        if request.form.get("date_selection"):
            date_filters = date_intervals.get(request.form.get("date_selection"))
            coo = get_coordinates(db_manager.get_euro_tweets_geo_by_date(date_filters))
        elif request.form.get("tag_selection"):
            tag_filter = tag_selections.get(request.form.get("tag_selection"))
            coo = get_coordinates(db_manager.get_euro_tweets_geo_by_tag(tag_filter))
        elif request.form.get("language_selection"):
            language_filter = request.form.get("language_selection")
            coo = get_coordinates(db_manager.get_euro_tweets_geo_by_language(language_filter))
        for coordinate in coo:
            markers.append({
                'icon': 'http://i.imgur.com/NJqz44X.png',
                'lat': coordinate['lat'],
                'lng': coordinate['lng'],
                'infobox': coordinate['text']}
            )
    return markers


def get_coordinates(records):
    coordinates = []
    for tweet in records:
        if parse_geo(tweet) is not None:
            longt, lat = parse_geo(tweet)
            coordinates.append({'lng':longt, 'lat':lat, 'text': tweet.geoinfo})
    return coordinates


def parse_geo(tweet):
    geos = tweet.geoinfo
    if delimiter in tweet.geoinfo:
        geos = tweet.geoinfo.split(delimiter)[1]
        #for geo in geos:
        #    coord = get_coordinates(geo)
        #    longt += float(coord[0])
        #    lat += float(coord[1])
        #return float(longt/2), float(lat/2)
    coord = parse_coordinates(geos)
    return float(coord[0]), float(coord[1])


def parse_coordinates(text):
    return re.findall(coordinates_regex, text)