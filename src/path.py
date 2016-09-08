import json

class EndOfPathError(Exception): pass

class Path:
    """
    Class that reads position data
    Functionality: Gets the requested position
    """
    def __init__(self, path):
        """Construct the path class. Reads the path file and extract the information
        """
        self._index = -1

        if path == None:
            raise ValueError
        else:
            with open(path, "r") as file:
                self.information = json.load(file)

    def next(self):
        try:
            self._index += 1
            x, y = self.get_position(self._index)
        except IndexError:
            raise EndOfPathError('End of path')
        return x, y

    def previous(self):
        try:
            self._index = max(-1, self._index-1)
            x, y = self.get_position(self._index)
        except IndexError:
            raise EndOfPathError('Before start of path')
        return x, y


    def get_position(self,n):
        """
        Returns a specific position on the path
        """
        position = self.information[n]
        x = position['Pose']['Position']['X']
        y = position['Pose']['Position']['Y']
        return x,y
