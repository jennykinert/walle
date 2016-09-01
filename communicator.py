"""
This class will handle the communication with the robot as in sending
json files back and forth.
"""
import json
import time
from http import client
from math import sin
from math import cos
from math import pi
from math import atan2

MRDS_URL = 'localhost:50000'
HEADERS = {"Content-type": "application/json", "Accept": "text/json"}

class UnexpectedResponse(Exception): pass

class Communicator:

    def __init__(self):
        self.mrds = client.HTTPConnection(MRDS_URL)

    def post_speed(self, angular_speed, linear_speed):
        params = json.dumps({'TargetAngularSpeed': angular_speed,
                             'TargetLinearSpeed':  linear_speed})
        self.mrds.request('POST', '/lokarria/differentialdrive', params, HEADERS)
        response = self.mrds.getresponse()
        status = response.status

        if status == 204:
            return response
        else:
            raise UnexpectedResponse(response)

    def get_laser_distance(self):
        self.mrds.request('GET','/lokarria/laser/echoes')
        response = self.mrds.getresponse()

        if (response.status == 200):
            laser_data = response.read()
            response.close()
            return json.loads(laser_data)
        else:
            return response

    def get_laser_angles(self):
        self.mrds.request('GET','/lokarria/laser/properties')
        response = self.mrds.getresponse()

        if (response.status == 200):
            laser_data = response.read()
            response.close()
            properties = json.loads(laser_data)
            beam_count = int((properties['EndAngle']-properties['StartAngle'])/properties['AngleIncrement'])
            a = properties['StartAngle']
            angles = []
            for i in range(beam_count):
                angles.append(a)
                a += properties['AngleIncrement']

            return angles
        else:
            raise UnexpectedResponse(response)

    def get_position(self):
        self.mrds.request('GET','/lokarria/localization')
        response = self.mrds.getresponse()
        if (response.status == 200):
            position_data = response.read()
            response.close()
            json_data = json.loads(poseData)
            x = json_data["Pose"]["Position"]["X"]
            y = json_data["Pose"]["Position"]["Y"]
            return x,y
        else:
            return UnexpectedResponse(response)
