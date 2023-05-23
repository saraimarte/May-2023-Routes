!curl ipecho.net/plain #gives IP address

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
newStops = pd.DataFrame({'Location':['347 Georges RD Dayton NJ 8810', '614 Cranbury RD East Brunswick NJ 8816', '1601 Perrineville RD Monzoe 08831', '651 Ridge RD Monomouth Junction 8852', '44 Obert ST South River NJ 8882 Post Office']})

#newStops = pd.DataFrame({'Location':['614 Cranbury RD East Brunswick NJ 8816']}) #v2 demo data testing for newStop placement 
#newStops = pd.DataFrame({'Location':['347 Georges RD Dayton NJ 8810']}) #v1 demo data

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
                return closest_location_Index
          closest_location_Index = findClosestLocation()
          print("CLOSEST LOCATION INDEX" + str(closest_location_Index))
          # i never called the function *cries* 

          def InsertIntoLocationsDf(locations,newStop, closest_location_Index):
                print("Finding the index of the closest location for this current new stop")
                #closestLocationIndex = indicesOfTheClosestLocations[currentnewStopCount]
                print("This is the index of the closest Location: " + str(closest_location_Index))
              
                locationsArray = locations.values
                maxIndexofDf = len(locations) -1

                print("Time to insert new stop in the route...")
                previousLocationIndex= closest_location_Index - 1
                nextLocation = closest_location_Index + 1
                beforePreviousIndex = closest_location_Index - 2

                a = locations['Location'][beforePreviousIndex]
                b = locations['Location'][previousLocationIndex]
                c = locations['Location'][closest_location_Index] 
                d= newStop
                e = locations['Location'][nextLocation] 
                print("a: " + a ) 
                print("b: " + b )
                print("c: " + c )
                print("d: " + d )

                #DURATION 1 (PLACING NEW STOP BEFORE CLOSEST STOP)
                
                #1. Find distance between a and b
                response_json = gmaps.distance_matrix(a, b, mode='driving', departure_time=datetime.now())
                distanceAB = response_json['rows'][0]['elements'][0]['duration']['value']

                #2. Find distance b and c 
                response_json = gmaps.distance_matrix(b, d, mode='driving', departure_time=datetime.now())
                distanceBD = response_json['rows'][0]['elements'][0]['duration']['value']     
                #3. Find distance between c and d
                response_json = gmaps.distance_matrix(d, c, mode='driving', departure_time=datetime.now())
                distanceDC= response_json['rows'][0]['elements'][0]['duration']['value'] 

                #4. Find distance between d and e
                response_json = gmaps.distance_matrix(c, e, mode='driving', departure_time=datetime.now())
                distanceCE= response_json['rows'][0]['elements'][0]['duration']['value'] 

                duration1 = distanceAB + distanceBD + distanceDC + distanceCE
                print("Duration 1 (if newstop is placed before closest location): " + str(duration1))

                #DURATION 2 (PLACING NEW STOP AFTER CLOSEST STOP)

                #1. Find distance between a and b
                response_json = gmaps.distance_matrix(a, b, mode='driving', departure_time=datetime.now())
                distanceAB = response_json['rows'][0]['elements'][0]['duration']['value']

                #2. Find distance b and c 
                response_json = gmaps.distance_matrix(b, c, mode='driving', departure_time=datetime.now())
                distanceBC = response_json['rows'][0]['elements'][0]['duration']['value']     
                #3. Find distance between c and d
                response_json = gmaps.distance_matrix(c, d, mode='driving', departure_time=datetime.now())
                distanceCD= response_json['rows'][0]['elements'][0]['duration']['value'] 

                #4. Find distance between d and e
                response_json = gmaps.distance_matrix(d, e, mode='driving', departure_time=datetime.now())
                distanceDE= response_json['rows'][0]['elements'][0]['duration']['value'] 
                
                duration2 = distanceAB + distanceBC + distanceCD + distanceDE
                print("Duration 2 (if newstop is placed after closest location): " + str(duration2))


                if duration1 < duration2: #if placing the newStop before the closest location makes the route shorter than put it before (so replace the closest so that the closest just goes down 1)
                    print("Duration 1 is Less than Duration 2 so putting the new stop before the closest location will make the route shorter")
                    modifiedIndex = closest_location_Index #putting it right before
                    if modifiedIndex <= maxIndexofDf:
                      print("Inserting Now... (before)")
                      locationsArray = np.insert(locationsArray, modifiedIndex, values = [f'{newStop}'], axis = 0)
                      locations = pd.DataFrame(locationsArray, columns = ['Location'])
                    elif modifiedIndex > maxIndexofDf:
                      print("Appending Now...")
                      new_row = pd.DataFrame({'Location':[f'{newStop}']})
                      locations = pd.concat([locations, new_row],ignore_index = True)
                elif duration1 > duration2:  #if placing the newStop before the closest location makes the route longer than put it after
                    print("Duration 1 is Greater than Duration 2 so putting the new stop before the closest location  will make the route longer")
                    modifiedIndex = closest_location_Index + 1 #putting it right after
                    if modifiedIndex <= maxIndexofDf:
                      print("Inserting Now... (after)")
                      locationsArray = np.insert(locationsArray, modifiedIndex, values = [f'{newStop}'], axis = 0)
                      locations = pd.DataFrame(locationsArray, columns = ['Location'])
                    elif modifiedIndex > maxIndexofDf:
                      print("Appending Now...")
                      new_row = pd.DataFrame({'Location':[f'{newStop}']})
                      locations = pd.concat([locations, new_row],ignore_index = True)
                else: 
                    print("Placing the newStop before or after its closest location does not seem to make a difference")
                    modifiedIndex = closest_location_Index + 1 #putting it right after
                    if modifiedIndex <= maxIndexofDf:
                      locationsArray = np.insert(locationsArray, modifiedIndex, values = [f'{newStop}'], axis = 0)
                      locations = pd.DataFrame(locationsArray, columns = ['Location'])
                    elif modifiedIndex > maxIndexofDf:
                      new_row = pd.DataFrame({'Location':[f'{newStop}']})
                      locations = pd.concat([locations, new_row],ignore_index = True)
                return locations
          locations = InsertIntoLocationsDf(locations, newStop, closest_location_Index)
          locations.to_csv("newRoute.csv")

          currentnewStopCount +=1;
      
closestLocations
newStops.head()
