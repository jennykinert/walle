"""Low level control"""

Kp = .01
Ki = .01
Kd = .01


class Distance:

    def __init__(self, length):
        self._error = length
        self._error1 = self._error
        self._error2 = self._error1

        self._m = 0
        self._m1 = self._m

    def new_speed(self, length):
        self._error2 = self._error1
        self._error1 = self._error
        self._error = length

        """
        delta_m = Kp*(self._error - self._error1) \
                  + Ki*self._error \
                  + Kd*(self._error - self._error1 + self._error2) 
        self._m = self._m1 + delta_m
        """
        self._m = pid(self._error, self._error1, self._error2, self._m)
        print(self._m)
        return self._m



def pid(e, e1, e2, m1):
    delta_m = Kp*(e - e1) \
              + Ki*e \
              + Kd*(e - e1 + e2) 
    return m1 + delta_m
