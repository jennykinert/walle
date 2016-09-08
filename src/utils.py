import math

# --------------------------------
# Angles                         -
# --------------------------------

def angle_between_two_points(x1, y1, x2, y2):
    """Return radians from -π to π"""
    return math.atan2(y2-y1, x2-x1)

def distance_between_two_points(x1, y1, x2, y2):
    """Calculate distance between two points"""
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def angle_within(angle1, angle2, range=math.pi/2):
    """Checks if angel1 is within +/-range (default π/2) of angle2"""
    angle1 = normalize_angle(angle1)
    lower = normalize_angle(angle2-range)
    upper = normalize_angle(angle2+range)

    if (abs(angle1 - lower) > math.pi):
        lower_condition = lower > angle1
    else:
        lower_condition = lower < angle1

    if (abs(angle1 - upper) > math.pi):
        upper_condition = angle1 > upper
    else:
        upper_condition = angle1 < upper

    return lower_condition and upper_condition

def normalize_angle(angle):
    """Return angle within -π to π"""
    if angle > math.pi:
        while angle > math.pi: angle -= 2*math.pi
        return angle
    elif angle < -math.pi:
        while angle < -math.pi: angle += 2*math.pi
        return angle
    else:
        return angle

def angle_difference(angle1, angle2):
    """Return shortest angle between two angles"""
    diff = angle1 - angle2
    diff = ((diff + math.pi) % (math.pi*2)) - math.pi
    return diff * -1

def translate_coordinates_between_systems(global_x, global_y, local_x, local_y, diff_angle):
    diff_angle = normalize_angle(diff_angle)
    xdiff = global_x-local_x
    ydiff = global_y-local_y
    
    angle_diff_point = math.atan2(ydiff,xdiff)
    length_diff_point= math.sqrt(xdiff**2+ydiff**2)
    angle_robot_point = angle_diff_point - diff_angle
    x_robot_point = math.cos(angle_robot_point)*length_diff_point
    y_robot_point = math.sin(angle_robot_point)*length_diff_point
    return x_robot_point, y_robot_point

def translate_coordinates_between_systems2(global_x, global_y, local_x, local_y, diff_angle):
    #diff_angle *= -1
    global_x *= -1
    global_y *= -1
    x = global_x + local_x * math.cos(diff_angle) - local_y * math.sin(diff_angle)
    y = global_y + local_x * math.sin(diff_angle) + local_y * math.cos(diff_angle)
    return x, y




# --------------------------------
# Vectors                        -
# --------------------------------

def heading(quaternion):
    return rotate(quaternion,{'X':1.0,'Y':0.0,"Z":0.0})

def rotate(q,v):
    return vector(qmult(qmult(q,quaternion(v)),conjugate(q)))

def quaternion(v):
    q=v.copy()
    q['W']=0.0;
    return q

def vector(q):
    v={}
    v['X']=q['X']
    v['Y']=q['Y']
    v['Z']=q['Z']
    return v

def conjugate(q):
    qc=q.copy()
    qc['X']=-q['X']
    qc['Y']=-q['Y']
    qc['Z']=-q['Z']
    return qc

def qmult(q1,q2):
    q={}
    q['W']=q1['W']*q2['W']-q1['X']*q2['X']-q1['Y']*q2['Y']-q1['Z']*q2['Z']
    q['X']=q1['W']*q2['X']+q1['X']*q2['W']+q1['Y']*q2['Z']-q1['Z']*q2['Y']
    q['Y']=q1['W']*q2['Y']-q1['X']*q2['Z']+q1['Y']*q2['W']+q1['Z']*q2['X']
    q['Z']=q1['W']*q2['Z']+q1['X']*q2['Y']-q1['Y']*q2['X']+q1['Z']*q2['W']
    return q
