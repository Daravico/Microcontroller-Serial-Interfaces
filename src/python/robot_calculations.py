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
    MHRz = HRz(theta)
    MHTz = HTz(d)
    MHTx = HTx(a)
    MHRx = HRx(alpha)

    



# ------------------------------------------------------------------------

def effector_final():
    pass

# ------------------------------------------------------------------------

print(HRz(np.pi/3) * HRz(np.pi/2*0)) 