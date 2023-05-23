#@title Imports
!pip install googlemaps
import pandas as pd
import googlemaps
from itertools import tee
from datetime import datetime
import requests
import json
import numpy as np

locations = pd.read_csv("locations.csv")
#newStops = pd.DataFrame({'Location':['347 Georges RD Dayton NJ 8810']})
newStops = pd.DataFrame({'Location':['347 Georges RD Dayton NJ 8810', '614 Cranbury RD East Brunswick NJ 8816', '1601 Perrineville RD Monzoe 08831', '651 Ridge RD Monomouth Junction 8852', '44 Obert ST South River NJ 8882 Post Office']})


#@title API 
API_KEY = 'API_KEY'
gmaps = googlemaps.Client(key = API_KEY)

#@title Script
closestLocations = []
newDistances = []
newDuration = []
newDistancesInText= []
newDurationInText= []

currentLocationCount = 0
currentnewStopCount = 0
indicesOfTheClosestLocations = []

for newStop in newStops['Location']: #for the newstop
  locationChoices = []
  durationChoices = []
  durationChoicesTextVersion = []
  distanceChoices = []
  distanceChoicesInText = []
  indicesOfLocationChoices = []
  print("Current NewStop: " + newStop)
  print("NEW STOP NUMBER: " + str(currentnewStopCount))
  for location in locations['Location']: #go through every location
    indicesOfLocationChoices.append(currentLocationCount)

    print("NEW LOCATION COUNT: " + str(currentLocationCount))
    print("Current Location: " + location)
    def findDistance(location,newStop): #find the distance between the newstop and the current location
       # url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={location}&destinations={newStop}&key={API_KEY}'
        #print(url)
        response_json = gmaps.distance_matrix(location, newStop, mode='driving', departure_time=datetime.now())
        print(response_json)  # Print the entire JSON response
        
        distance_text = response_json['rows'][0]['elements'][0]['distance']['text']
        duration_text = response_json['rows'][0]['elements'][0]['duration']['text']

        distance = response_json['rows'][0]['elements'][0]['distance']['value']
        duration = response_json['rows'][0]['elements'][0]['duration']['value']

        print("Calculating Distance Between New Stop and Current Location...")
        print("Distance Text: " + distance_text + ' Value: ' + str(distance))
        print("Calculating Duration Between New Stop and Current Location...")
        print("Duration Text:" + duration_text + ' Value: ' + str(duration))


        print("Inserting current distance between currentNewStop and currentLocation into distanceChoices array so we can later choose the distance that is closest to the newStop...")
        distanceChoices.append(distance)
        print("Updated distanceChoices List " +  str(distanceChoices))
        print("Inserting corresponding location to locationChoices so when we  find the closest location's index from distanceChoices we can get the actual location by the same index in locationChoices..")
        locationChoices.append(location)
        durationChoices.append(duration)
        print("Updated Locations Choices:")
        print(locationChoices)
        durationChoicesTextVersion.append(duration_text)
        distanceChoicesInText.append(distance_text)
        
    findDistance(location,newStop)
    currentLocationCount += 1
  #After going through all the locations find the location that has the shortest distance
  print("After going through all the locations lets find which one is closest to the newStop...")
  def findClosestLocation():
      print("Choosing the smallest distance from distanceChoices... getting the index...")
      closest_location_Index = distanceChoices.index(min(distanceChoices))  # find the location that has the shortest distance from the newStop
      print("Smallest Distance Index: " + str(closest_location_Index) )
      print("Choosing the closest location from locationChoices... adding the location into closestLocations array... ")
      closestLocations.append(locationChoices[closest_location_Index]) #add that location to the closestLocations list.
      print("Updated closestLocations: ")
      print(closestLocations)
      print("Updating the corresponding distance of  the closets locaton to the newStop...")
      newDistances.append(distanceChoices[closest_location_Index])
      newDistancesInText.append(distanceChoicesInText[closest_location_Index])
      print("newDistances ")
      print(newDistances)
      print("Updating the corresponding duration of  the closet location to the newStop...")
      newDuration.append(durationChoices[closest_location_Index])
      newDurationInText.append(durationChoicesTextVersion[closest_location_Index])
      print("New Duration: ")
      print(newDistances)
      print("Inserting the index of the closest location to the newStop in indicesOfTheClosestLocations...")
      indicesOfTheClosestLocations.append(closest_location_Index) 
      print("THESE ARE THE INDICIES OF THE CLOSEST LOCATIONS: ")
      print(indicesOfTheClosestLocations)
      print("The Location with the shortest distance to " + newStop + " is " + location + " with " + str(distanceChoices[closest_location_Index]) + " meters.")
  findClosestLocation() # i never called the function *cries*
  print("Now Im going to insert the current newStop right after the closest location in the original dataframe...")


  def InsertIntoLocationsDf(locations):
    print("Finding the index of the closest location for this current new stop")
    closestLocationIndex = indicesOfTheClosestLocations[currentnewStopCount]
    print("This is the index of the closest Location: " + str(closestLocationIndex))
    print("Inserting the newStop right after it...")
    modifiedIndex = closestLocationIndex + 1 #putting it right after
    locationsArray = locations.values
    maxIndexofDf = len(locations) -1
    if modifiedIndex <= maxIndexofDf:
      locationsArray = np.insert(locationsArray, modifiedIndex, values = [f'{newStop}'], axis = 0)
      locations = pd.DataFrame(locationsArray, columns = ['Location'])
    elif modifiedIndex > maxIndexofDf:
      new_row = pd.DataFrame({'Location':[f'{newStop}']})
      locations = pd.concat([locations, new_row],ignore_index = True )
    return locations
  locations = InsertIntoLocationsDf(locations)
  currentnewStopCount +=1;
