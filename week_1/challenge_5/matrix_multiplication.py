# matrix_multiplication.py

import numpy as np

def matrix_multiply(A, B):
    return np.dot(A, B)

if __name__ == "__main__":
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    result = matrix_multiply(A, B)
    print("Matrix Multiplication Result:\n", result)
