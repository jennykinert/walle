class Path:
    """
    Class that reads position data
    Functionality: Gets the requested position
    """
    def __init__(self, path):
        """Construct the path class. Reads the path file and extract the information
        """
        self.path = path
        if self.path == None:
            raise ValueError
        else:
            with open(self.path, "r") as file:
                self.information = json.load(file)

    def get_position(self,n):
        """
        Returns a specific position on the path
        """
        position = self.information[n]
        x = position['Pose']['Position']['X']
        y = position['Pose']['Position']['Y']
        return x,y
