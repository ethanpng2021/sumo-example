###This is to be run on the Sumo server.
import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd


def getdatetime():
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
        DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        return DATIME

PORT = 8813
sumoCmd = ["sumo-gui", "-c", "osm.sumocfg", "--num-clients", "2"]
traci.start(sumoCmd, PORT)
traci.setOrder(1) # number can be anything as long as each client gets its own number

while traci.simulation.getMinExpectedNumber() > 0:
       
        traci.simulationStep();

        vehicles=traci.vehicle.getIDList();
        trafficlights=traci.trafficlight.getIDList();

        for i in range(0,len(vehicles)):

                #Function descriptions
                #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
                #https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-getSpeed
                vehid = vehicles[i]
                x, y = traci.vehicle.getPosition(vehicles[i])
                coord = [x, y]
                lon, lat = traci.simulation.convertGeo(x, y)
                gpscoord = [lon, lat]
                spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
                edge = traci.vehicle.getRoadID(vehicles[i])
                lane = traci.vehicle.getLaneID(vehicles[i])
                displacement = round(traci.vehicle.getDistance(vehicles[i]),2)
                turnAngle = round(traci.vehicle.getAngle(vehicles[i]),2)
                nextTLS = traci.vehicle.getNextTLS(vehicles[i])

                #Packing of all the data for export to CSV/XLSX
                vehList = [getdatetime(), vehid, coord, gpscoord, spd, edge, lane, displacement, turnAngle, nextTLS]
                
                
                print("Vehicle: ", vehicles[i], " at datetime: ", getdatetime())
                print(vehicles[i], " >>> Position: ", coord, " | GPS Position: ", gpscoord, " |", \
                                       " Speed: ", round(traci.vehicle.getSpeed(vehicles[i])*3.6,2), "km/h |", \
                                      #Returns the id of the edge the named vehicle was at within the last step.
                                       " EdgeID of veh: ", traci.vehicle.getRoadID(vehicles[i]), " |", \
                                      #Returns the id of the lane the named vehicle was at within the last step.
                                       " LaneID of veh: ", traci.vehicle.getLaneID(vehicles[i]), " |", \
                                      #Returns the distance to the starting point like an odometer.
                                       " Distance: ", round(traci.vehicle.getDistance(vehicles[i]),2), "m |", \
                                      #Returns the angle in degrees of the named vehicle within the last step.
                                       " Vehicle orientation: ", round(traci.vehicle.getAngle(vehicles[i]),2), "deg |", \
                                      #Return list of upcoming traffic lights [(tlsID, tlsIndex, distance, state), ...]
                                       " Upcoming traffic lights: ", traci.vehicle.getNextTLS(vehicles[i]), \
                       )

   
traci.close()
