import numpy as np
from typing import List

# DEFAULT VALUES:
# DH Parameters and Homogeneous Matrix variables.
q = [0,             np.pi / 2,      0]
d = [60,            0,              0]
a = [0,             105,            100]
A = [np.pi / 2,     0,              0]

ranges = np.array([[-np.pi / 2, np.pi / 2], [0, np.pi / 2], [0, np.pi / 2]])


# ------------------------------------------------------------------------
class RoboticProperties:
    """
    Conteiner for properties. Functions
    """

    def __init__(
        self,
        q: List[float] = q,
        d: List[float] = d,
        a: List[float] = a,
        A: List[float] = A,
        ranges: List[List[float]] = ranges,
    ):
        """ """

        # TODO: Add a note that this can be changed according to the user/developer/robot.
        self.dof_upp_limit = 6
        self.dof_inf_limit = 1

        # Extracted degrees of freedom from the previous list (All must be the same).
        self.degrees_of_freedom = len(q)

        # Pointer to the actuators, active axis in the DH parameters (Either index 0 or 1). By default, Q's.
        self.pointer_actuators = np.zeros(3)

        # Saving the information about the ranges for the joints.
        self.ranges = ranges

        # Initialization of DH table for the previous parameters.
        self.dh_params = np.empty((self.degrees_of_freedom, 4))

        # Saving the values.
        self.dh_params[:, 0] = q
        self.dh_params[:, 1] = d
        self.dh_params[:, 2] = a
        self.dh_params[:, 3] = A

        # Default table for the DH parameters.
        self.dh_params_active_table = np.copy(self.dh_params)

        # Initialization of N empty arrays depending on the degrees of freedom.
        self.DH_matrix_array = np.array(
            [np.empty((4, 4)) for _ in range(self.degrees_of_freedom)]
        )

        # Initialization of the final matrix for the DH parameters.
        self.final_transformation_matrix = np.eye(4)

        # Initialization of the position for the final efector.
        self.final_efector_vector = np.array([0, 0, 0])

        # Setting the default configuration.
        self.default_configuration_request()

    # ------------------------------------------------------------------------

    def matrix_rounder(self, matrix: np.ndarray, digits: int):
        """
        This function helps in reducing the amount of digits being
        displayed in the terminal.

        :matrix(np.ndarray): Array to be converted.
        :digits(int): Number of digits to be rounded up to (Power of 10).
        """

        ten_digits = np.power(10, digits)

        new_matrix = np.round(matrix * ten_digits) / ten_digits

        return new_matrix

    # ------------------------------------------------------------------------

    def mapper(x: float, x1: float, x2: float, y1: float, y2: float):
        """
        This function helps in getting the linear mapping for values in a
        certain range (x1→y1 >> x2→y2).
        """
        m = (y2 - y1) / (x2 - x1)

        y = m * (x - x1) + y1

        return y
    
    # ------------------------------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # D I R E C T   K I N E M A T I C S
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    """
    The following functions are used to calculate the homogeneous
    transformation matrices, using the Denavit Hartenberg parameters
    (theta, d, a, alpha) for the rotations and translations in the
    X and Z axes. The resulting matrix is returned for each case.
    """
    # ------------------------------------------------------------------------

    def HRz(self, theta: float):
        matrix = np.array(
            [
                [np.cos(theta), -np.sin(theta), 0, 0],
                [np.sin(theta), np.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        rounded_matrix = self.matrix_rounder(matrix, 5)
        return rounded_matrix

    # ------------------------------------------------------------------------

    def HRx(self, alpha: float):
        matrix = np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(alpha), -np.sin(alpha), 0],
                [0, np.sin(alpha), np.cos(alpha), 0],
                [0, 0, 0, 1],
            ]
        )

        rounded_matrix = self.matrix_rounder(matrix, 2)
        return rounded_matrix

    # ------------------------------------------------------------------------

    def HTx(self, a: float):
        matrix = np.array([[1, 0, 0, a], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        rounded_matrix = self.matrix_rounder(matrix, 2)
        return rounded_matrix

    # ------------------------------------------------------------------------

    def HTz(self, d: float):
        matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, d], [0, 0, 0, 1]])

        rounded_matrix = self.matrix_rounder(matrix, 2)
        return rounded_matrix

    # ------------------------------------------------------------------------

    def DH(self, theta: float, d: float, a: float, alpha: float):
        """
        The final Homogenous Transformation Matrix for the Denavit Hartenberg
        procedure is calculated using the corresponding parameters for the
        connection between two frames.

        :theta(float): Angular value for the Rz transformation.
        :d(float): Linear value for the Tz transformation.
        :a(float): Linear value for the Tx transformation.
        :alpha(float): Angular value for the Rx transformation.
        """
        Matrix_HRz = self.HRz(theta)
        Matrix_HTz = self.HTz(d)
        Matrix_HTx = self.HTx(a)
        Matrix_HRx = self.HRx(alpha)

        DH_matrix = Matrix_HRz @ Matrix_HTz @ Matrix_HTx @ Matrix_HRx

        return DH_matrix

    # ------------------------------------------------------------------------

    def end_effector_position(self, DH_matrix: np.ndarray):
        """
        Uses the Denavit Hartenberg matrix to calculate the position of the
        final part of the robot. Coordinates in the last frame are considered as
        the origin (0,0,0).

        :DH_matrix(np.ndarray): Matrix to work with.
        """
        origin = np.array([0, 0, 0, 1]).reshape(4, 1)

        position = DH_matrix * origin

        return position

    # ------------------------------------------------------------------------

    def default_configuration_request(self):
        """
        Sets the default configuration for the DH parameters and the starting settings
        for the transformation matrices and the end effector position values.
        """
        # Setting the default DH parameters.
        self.dh_params_active_table = np.copy(self.dh_params)

        # Setting the new size of transformation matrices required (by DoF).
        self.DH_matrix_array = np.array(
            [np.empty((4, 4)) for _ in range(self.degrees_of_freedom)]
        )

        # Setting the starting transformation matrix and end effector position vector.
        self.update_matrices_request()

    # ------------------------------------------------------------------------

    def update_dh_table_request(self, value: float, row: int):
        # Gathering the column to be affected.
        actuator_col = int(self.pointer_actuators[row])

        # Updating the value.
        self.dh_params_active_table[row, actuator_col] = value

    # ------------------------------------------------------------------------

    def update_matrices_request(self):
        '''
        When the function is called the DH parameters are extracted to calculate the 
        transformation matrices. Later it is set the final transformation matrix with 
        the resulting ones from each frame (M_0↔N = M_0↔1 * M_1↔2 * ... * M_N-1↔N). 
        The final effector vector position is also calculated.
        '''
        # Denavit-Hartenberg parameters.
        q = self.dh_params_active_table[:, 0]
        d = self.dh_params_active_table[:, 1]
        a = self.dh_params_active_table[:, 2]
        A = self.dh_params_active_table[:, 3]

        # Final transformation matrix is reset.
        self.final_transformation_matrix = np.eye(4)

        for i in range(self.degrees_of_freedom):
            # Homegeneous transformation matrix.
            self.DH_matrix_array[i] = self.DH(q[i], d[i], a[i], A[i])
            self.final_transformation_matrix = (
                self.final_transformation_matrix @ self.DH_matrix_array[i]
            )

        # Final effector position.
        self.final_efector_vector = self.final_transformation_matrix[0:3, 3]

    # ------------------------------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # I N V E R S E   K I N E M A T I C S
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


if __name__ == "__main__":

    q = [0, np.pi / 2, 0]
    d = [3, 0, 0]
    a = [0, 5, 4]
    A = [np.pi / 2, 0, 0]

    ranges = [[-90, 90], [0, 90], [0, 90]]

    robotics = RoboticProperties(q, d, a, A, ranges)
