import googlemaps
from datetime import datetime
gmaps = googlemaps.Client(key=os.environ['DIRECTIONS_KEY'])

def getDirections(fromLocation, toLocation, mode, language):
    directions = ""
    directions_result = gmaps.directions(fromLocation,toLocation,mode=mode, departure_time=datetime.now(), language=language)
    for steps in directions_result[0]['legs'][0]['steps']:
        step = steps['html_instructions'].replace("<b>","")
        step = step.replace("</b>", "")
        directions += step + ". "
    return directions
