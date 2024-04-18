import numpy as np

# ------------------------------------------------------------------------

def matrix_rounder(matrix: np.ndarray, digits: int):
    '''
    This function helps in reducing the amount of digits being
    displayed in the terminal.

    :matrix(np.ndarray): Array to be converted.
    :digits(int): Number of digits to be rounded up to (Power of 10).
    '''

    ten_digits = np.power(10, digits)

    new_matrix = np.round(matrix * ten_digits) / ten_digits

    return new_matrix


# ------------------------------------------------------------------------
'''
The following functions are used to calculate the homogeneous
transformation matrices, using the Denavit Hartenberg parameters
(theta, d, a, alpha) for the rotations and translations in the
X and Z axes. The resulting matrix is returned for each case.
'''
# ------------------------------------------------------------------------

def HRz(theta: float):
    matrix = np.array([
        [   np.cos(theta),     -np.sin(theta),     0,                  0               ],
        [   np.sin(theta),     np.cos(theta),      0,                  0               ],
        [   0,                 0,                  1,                  0               ],
        [   0,                 0,                  0,                  1               ]
    ])

    rounded_matrix = matrix_rounder(matrix, 5) 
    return rounded_matrix

# ------------------------------------------------------------------------

def HRx(alpha: float):
    matrix = np.array([
        [   1,                 0,                  0,                  0               ],
        [   0,                 np.cos(alpha),      -np.sin(alpha),     0               ],
        [   0,                 np.sin(alpha),      np.cos(alpha),      0               ],
        [   0,                 0,                  0,                  1               ]
    ])

    rounded_matrix = matrix_rounder(matrix, 2) 
    return rounded_matrix

# ------------------------------------------------------------------------

def HTx(a: float):
    matrix = np.array([
        [   1,                 0,                  0,                  a               ],
        [   0,                 1,                  1,                  0               ],
        [   0,                 1,                  1,                  0               ],
        [   0,                 0,                  0,                  1               ]
    ])

    rounded_matrix = matrix_rounder(matrix, 2) 
    return rounded_matrix

# ------------------------------------------------------------------------

def HTz(d: float):
    matrix = np.array([
        [   1,                 0,                  0,                  0               ],
        [   0,                 1,                  1,                  0               ],
        [   0,                 1,                  1,                  d               ],
        [   0,                 0,                  0,                  1               ]
    ])

    rounded_matrix = matrix_rounder(matrix, 2) 
    return rounded_matrix

# ------------------------------------------------------------------------

def DH(theta: float, d: float, a: float, alpha: float):
    '''
    The final Homogenous Transformation Matrix for the Denavit Hartenberg 
    procedure is calculated using the corresponding parameters for the 
    connection between two frames.

    :theta(float): Angular value for the Rz transformation.
    :d(float): Linear value for the Tz transformation.
    :a(float): Linear value for the Tx transformation.
    :alpha(float): Angular value for the Rx transformation.
    '''
    MHRz = HRz(theta)
    MHTz = HTz(d)
    MHTx = HTx(a)
    MHRx = HRx(alpha)

    DH_matrix = MHRz @ MHTz @ MHTx @ MHRx

    return DH_matrix
    
# ------------------------------------------------------------------------

def end_effector_position(DH_matrix: np.ndarray):
    '''
    Uses the Denavit Hartenberg matrix to calculate the position of the 
    final part of the robot. Coordinates in the last frame are considered as
    the origin (0,0,0).

    :DH_matrix(np.ndarray): Matrix to work with.
    '''
    origin = np.array([0, 0, 0, 1]).reshape(4,1)

    position = DH_matrix * origin

    return position

# ------------------------------------------------------------------------

def Mapper(x: float, x1: float, x2: float, y1: float, y2: float):
    '''
    This function helps in getting the linear mapping for values in a
    certain range (x1→y1 >> x2→y2).
    '''
    m = (y2 - y1 ) / (x2 - x1)

    y = m * (x - x1) + y1

    return y

DH1 = DH(np.pi/3, 5, 3, 0)
print(DH1)
