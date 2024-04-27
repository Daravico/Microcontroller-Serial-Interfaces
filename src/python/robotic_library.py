import numpy as np
from typing import List

# FIXME: Make 3 classes, one for robotic properties, which can also be a struct to store the values.
# Or have it to be a class to have the methods to change things according to the updates.

# Have a class for handling Direct Kinematic functions.

# Have a class for handling Inverse Kinematic functions.

# ------------------------------------------------------------------------
class RoboticProperties:
    '''
    Conteiner for properties. Functions
    '''

    def __init__(self, q:List[float], d:List[float], a:List[float], A:List[float], ranges:List[List[float]]):
        '''

        '''

        self.q = q
        self.d = d
        self.a = a
        self.A = A

        # Extracted degrees of freedom from the previous list (All must be the same).
        self.degrees_of_freedom = len(q)

        # Saving the information about the ranges for the joints.
        self.ranges = ranges

        # Initialization of DH table for the previous parameters.
        self.DH_parameters_table = np.empty((self.degrees_of_freedom, 4))

        # Initialization of N empty arrays depending on the degrees of freedom.
        self.DH_matrix_array = np.array([np.empty((4,4)) for _ in range(self.degrees_of_freedom)])
        
        # Initialization of the final matrix for the DH parameters.
        self.final_transformation_matrix = np.eye(4)

        # Initialization of the position for the final efector.
        self.final_efector_vector = np.array([0,0,0])

        self.update_tables(q, d, a, A)

    # ------------------------------------------------------------------------

    def update_tables(self, q:List[float], d:List[float], a:List[float], A:List[float]):
        '''
        
        '''
        
        for i in range(self.degrees_of_freedom):
            # Denavit-Hartenberg parameters.
            self.DH_parameters_table[i,0] = q[i]
            self.DH_parameters_table[i,1] = d[i]
            self.DH_parameters_table[i,2] = a[i]
            self.DH_parameters_table[i,3] = A[i]

            # Homegeneous transformation matrix.
            self.DH_matrix_array[i] = self.DH(q[i], d[i], a[i], A[i])
            self.final_transformation_matrix = self.final_transformation_matrix @ self.DH_matrix_array[i]

    # ------------------------------------------------------------------------

    def matrix_rounder(self, matrix: np.ndarray, digits: int):
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

    def mapper(x: float, x1: float, x2: float, y1: float, y2: float):
        '''
        This function helps in getting the linear mapping for values in a
        certain range (x1→y1 >> x2→y2).
        '''
        m = (y2 - y1 ) / (x2 - x1)

        y = m * (x - x1) + y1

        return y
    
    # ------------------------------------------------------------------------

    def joint_degrees():
        pass
    
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # D I R E C T   K I N E M A T I C S
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    
    '''
    The following functions are used to calculate the homogeneous
    transformation matrices, using the Denavit Hartenberg parameters
    (theta, d, a, alpha) for the rotations and translations in the
    X and Z axes. The resulting matrix is returned for each case.
    '''
    # ------------------------------------------------------------------------

    def HRz(self, theta: float):
        matrix = np.array([
            [   np.cos(theta),     -np.sin(theta),     0,                  0               ],
            [   np.sin(theta),     np.cos(theta),      0,                  0               ],
            [   0,                 0,                  1,                  0               ],
            [   0,                 0,                  0,                  1               ]
        ])

        rounded_matrix = self.matrix_rounder(matrix, 5) 
        return rounded_matrix

    # ------------------------------------------------------------------------

    def HRx(self, alpha: float):
        matrix = np.array([
            [   1,                 0,                  0,                  0               ],
            [   0,                 np.cos(alpha),      -np.sin(alpha),     0               ],
            [   0,                 np.sin(alpha),      np.cos(alpha),      0               ],
            [   0,                 0,                  0,                  1               ]
        ])

        rounded_matrix = self.matrix_rounder(matrix, 2) 
        return rounded_matrix

    # ------------------------------------------------------------------------

    def HTx(self, a: float):
        matrix = np.array([
            [   1,                 0,                  0,                  a               ],
            [   0,                 1,                  0,                  0               ],
            [   0,                 0,                  1,                  0               ],
            [   0,                 0,                  0,                  1               ]
        ])

        rounded_matrix = self.matrix_rounder(matrix, 2) 
        return rounded_matrix

    # ------------------------------------------------------------------------

    def HTz(self, d: float):
        matrix = np.array([
            [   1,                 0,                  0,                  0               ],
            [   0,                 1,                  0,                  0               ],
            [   0,                 0,                  1,                  d               ],
            [   0,                 0,                  0,                  1               ]
        ])

        rounded_matrix = self.matrix_rounder(matrix, 2) 
        return rounded_matrix

    # ------------------------------------------------------------------------

    def DH(self, theta: float, d: float, a: float, alpha: float):
        '''
        The final Homogenous Transformation Matrix for the Denavit Hartenberg 
        procedure is calculated using the corresponding parameters for the 
        connection between two frames.

        :theta(float): Angular value for the Rz transformation.
        :d(float): Linear value for the Tz transformation.
        :a(float): Linear value for the Tx transformation.
        :alpha(float): Angular value for the Rx transformation.
        '''
        Matrix_HRz = self.HRz(theta)
        Matrix_HTz = self.HTz(d)
        Matrix_HTx = self.HTx(a)
        Matrix_HRx = self.HRx(alpha)

        DH_matrix = Matrix_HRz @ Matrix_HTz @ Matrix_HTx @ Matrix_HRx

        return DH_matrix
        
    # ------------------------------------------------------------------------

    def end_effector_position(self, DH_matrix: np.ndarray):
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

    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # I N V E R S E   K I N E M A T I C S
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||




if __name__ == '__main__':

    q = [0,         np.pi/2,     0]
    d = [3,         0,           0]
    l = [0,         5,           4]
    A = [np.pi/2,   0,           0]

    ranges = [[-90, 90], [0, 90], [0, 90]]
    
    robotics = RoboticProperties(q, d, l, A, ranges)
