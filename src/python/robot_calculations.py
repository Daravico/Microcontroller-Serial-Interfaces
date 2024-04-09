import numpy as np

def HRz(theta):
    matrix = np.array([
        [1,     0,              0,              0],
        [0,     np.cos(theta),  -np.sin(theta), 0],
        [0,     np.sin(theta),  np.cos(theta),  0],
        [0,     0,              0,              1]
    ])

    return matrix

def HRx(alpha):
    matrix = np.array([
        [1,     0,              0,              0],
        [0,     np.cos(alpha),  -np.sin(alpha), 0],
        [0,     np.sin(alpha),  np.cos(alpha),  0],
        [0,     0,              0,              1]
    ])

    return matrix

def HTx():
    pass

def HTz():
    pass

def DH():
    pass

def effector_final():
    pass

print(HRx(np.pi))