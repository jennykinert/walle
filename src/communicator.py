
import json
from math import atan2
from http import client
from utils import heading

HEADERS = {'Content-type': 'application/json', 'Accept': 'text/json'}

class UnexpectedResponse(Exception): pass

class Communicator:
    """
    This class will handle the communication with the robot as in sending
    json files back and forth.
    """

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.mrds = client.HTTPConnection(host, port=port)

    def _send_post(self, url, params):
        try:
            self.mrds.request('POST', url, params, HEADERS)
        except BrokenPipeError:
            self.mrds = client.HTTPConnection(self._host, port=self._port)
            self.mrds.request('POST', url, params, HEADERS)

    def _send_get(self, url):
        try:
            self.mrds.request('GET', url)
        except BrokenPipeError:
            self.mrds = client.HTTPConnection(self._host, port=self._port)
            self.mrds.request('GET', url)


    def post_speed(self, angular_speed, linear_speed):
        """Set target speed and target angular speed on the robot"""

        params = json.dumps({'TargetAngularSpeed': angular_speed,
                             'TargetLinearSpeed':  linear_speed})

        self._send_post('/lokarria/differentialdrive', params)

        response = self.mrds.getresponse()
        status = response.status
        response.read().decode('utf-8') # Read all data to be able to reuse connection

        if status == 204:
            return
        else:
            raise UnexpectedResponse(response)

    def get_laser_distance(self):
        """Get the distance all lasers measuered, returned in a list"""
        self._send_get('/lokarria/laser/echoes')
        response = self.mrds.getresponse()

        if (response.status == 200):
            laser_data = response.read()
            return json.loads(laser_data.decode('utf-8'))['Echoes']
        else:
            return response

    def get_laser_angles(self):
        """Get angles of all lasers, returned in a list"""
        self._send_get('/lokarria/laser/properties')
        response = self.mrds.getresponse()

        if (response.status == 200):
            laser_data = response.read()
            properties = json.loads(laser_data.decode('utf-8'))
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
        """Get position of robot"""
        self._send_get('/lokarria/localization')
        response = self.mrds.getresponse()
        if (response.status == 200):
            position_data = response.read()
            json_data = json.loads(position_data.decode('utf-8'))
            x = json_data['Pose']['Position']['X']
            y = json_data['Pose']['Position']['Y']
            return x,y
        else:
            return UnexpectedResponse(response)

    def get_heading(self):
        """Returns the angle robot points"""
        self._send_get('/lokarria/localization')
        response = self.mrds.getresponse()
        if (response.status == 200):
            position_data = response.read()
            json_data = json.loads(position_data.decode('utf-8'))
            unit_vector = heading(json_data['Pose']['Orientation'])
            angle = atan2(unit_vector['Y'], unit_vector['X'])
            return angle
        else:
            return UnexpectedResponse(response)

