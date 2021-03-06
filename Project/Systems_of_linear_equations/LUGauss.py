#!/bin/python3

from pandas import DataFrame
from copy import deepcopy, copy
from numpy import linalg as LA

# El método principal es lu_gauss.
# Retorna 0 (exitoso), la matriz L, la matriz U, el vector resultado y los pasos
# Los pasos son: matriz Lz, vector Z y matriz Ux (de la cual sale el vector resultado)

class LU_gauss:
    mults = []

    def create_matrix_L(self, lenMatrix):
        global mults
        mults = [[0 for x in range(lenMatrix)] for y in range(lenMatrix)]

    def upper_triangular(self, A):
        global mults
        if LA.det(A) == 0:
            return 0        
        try:
            LA.inv(A)
        except LA.LinAlgError:
            return -1
        n = len(A)
        self.create_matrix_L(n)
        for i in range(0, n):
            for j in range(i, n):
                if i == j:
                    mults[i][i] = 1
                    column = [row[i] for row in A]
                    lenColumn = len(column)
                    if A[i][i] == 0:
                        for k in range(i, lenColumn):
                            if column[k] != 0:
                                aux = A[k]
                                A[k] = A[i]
                                A[i] = aux
                                break

                    helper = A[i][i]
                    if helper == 0:
                        return 1

                else:
                    helper = A[j][i]
                    mult = helper / A[i][i]
                    mults[j][i] = mult
                    row1 = A[i]
                    row2 = A[j]
                    for k in range(0, len(row2)):
                        row2[k] -= (mult * row1[k])
                    A[j] = row2
        return A

    def progressive_substitution(self, stepMat):
        vector = []
        n = len(stepMat)
        for x in range(n):
            vector.append(0)
        vector[0] = stepMat[0][n] / stepMat[0][0]
        i = 1
        while i <= n - 1:
            result = 0
            p = 0
            while p <= len(vector) - 1:
                result += (stepMat[i][p] * vector[p])
                p += 1
            vector[i] = stepMat[i][n] - result / stepMat[i][i]
            i += 1
        return vector

    def regressive_substitution(self, stepMat):
        n = len(stepMat)
        vector = []
        for x in range(n):
            vector.append(0)
        vector[n - 1] = stepMat[n - 1][n] / stepMat[n - 1][n - 1]
        i = n - 2
        while i >= 0:
            result = 0
            p = len(vector) - 1
            while p >= 0:
                result += (stepMat[i][p] * vector[p])
                p -= 1
            vector[i] = (stepMat[i][n] - result) / stepMat[i][i]
            i -= 1
        return vector

    def aumMatrix(self, A, b):
        cont = 0
        for i in A:
            i.append(b[cont])
            cont += 1
        return A

    def lu_gauss(self, A, vector):
        u_matrix = self.upper_triangular(A)
        if u_matrix == -1:
            return 1, "The matrix is not invertible"
        elif u_matrix == 1:
            return 1, "It's not possible to step the matrix"
        elif u_matrix == 0:
            return 1, "The matrix is not well conditioned. Determinant is ZERO"
        l_matrix = mults
        Lz = self.aumMatrix(l_matrix, vector)
        vector_z = self.progressive_substitution(Lz)
        Ux = self.aumMatrix(u_matrix, vector_z)
        result = self.regressive_substitution(Ux)
        return 0, l_matrix, u_matrix, result, Lz, vector_z, Ux

#A = [[2, -3, 4, 1], [-4, 2, 1, -2], [1, 3, -5, 3], [-3, -1, 1, -1]]
#b = [10, -10, 32, -21]
#A = [[-7, 2, -3, 4], [5, -1, 14, -1], [1, 9, -7, 5], [-12, 13, -8, -4]]
#b = [-12, 13, 31, -32]
#print(lu_gauss(A, b))

# lugauss = LU_gauss()
#
# name = input("Enter the name of the file you want the answer to be saved. It's going to have '.txt' extension: ")
# matrix_rows = int(input("As this has to be a square matrix, the number of rows is going to be the same number of columns. \
#                 \nEnter number of rows in the matrix: "))
# matrix = []
# vector = []
# print("Enter the %s x %s matrix: "% (matrix_rows, matrix_rows))
# print("Separe each number with a space and to change the row press ENTER")
# for j in range(matrix_rows):
#         matrix.append(list(map(float, input().rstrip().split())))
# print("Enter de vector. Separe each number with a space")
# vector.append(list(map(float, input().rstrip().split())))
# vector = vector[0]
# print("You will find the result in " + name + ".txt")
# matrix_aux = deepcopy(matrix)
# vector_aux = copy(vector)
# with open(name + ".txt", "w") as result:
#     print("The augmented matrix is:" , file=result)
#     print(DataFrame(lugauss.aumMatrix(matrix, vector)), file=result)
#     print("\n", file=result)
#     A = lugauss.lu_gauss(matrix_aux, vector_aux, result)[2]
#     print("The result of each variable is: ", file=result)
#     num = 1
#     for x in A:
#         print("x" + str(num) + " = " + str(x), file=result)
#         num += 1
    