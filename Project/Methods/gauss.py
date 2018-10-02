#!/bin/python3

from copy import deepcopy, copy
from pandas import DataFrame

def partial_pivot(A, k) 
    biggest = abs(A[k][k])
    biggest_row = k 
    n = len(A)
    for i in range(k+1, n):
        if abs(A[i][k]) > biggest:
            biggest = a[i][k]
            biggest_row = i

    if biggest == 0:
        print("No unique solution")
    elif not biggest_row == k:
        swap_rows(A, biggest_row, k)
    return A

def total_pivot(A, k):
    biggest = 0
    biggest_row = k
    biggest_column = k
    n = len(A)
    marks = []

    for i in range(0, n):
        marks[i] = i+1

    for i in range(k, n):
        for j in range(k, n):
            if abs(A[i][j]) > biggest:
                biggest = abs(A[i][j])
                biggest_row = i
                biggest_column = j

    if biggest == 0:
        print("No unique solution")
    else:
        if not biggest_row == k:
            A = swap_cols(A, biggest_row, k)
            tmp = marks[biggest_column]
            marks[biggest_column] = marks[k]
            marks[k] = tmp
    return A    

def swap_rows(A, rowa, rowb):
    tmp = A[rowa]
    A[rowa] = A[rowb]
    A[rowb] = tmp
    return A

def swap_cols(A, cola, colb):
    for i in range(0, len(A)):
        tmp = A[i][cola]
        A[i][cola] = A[i][colb]
        A[i][colb] = tmp
    return A



def stepped(A, b):
    Ab = aumMatrix(A, b)
    n = len(Ab) 
    for i in range (0, n):
        for j in range (i, n):
            if i == j:
                column = [row[i] for row in A]
                lenColumn = len(column)
                if all(v == 0 for v in column):
                    continue
                if A[i][i] == 0:
                    for k in range(i, lenColumn):
                        if column[k] != 0:
                            aux = A[k]
                            A[k] = A[i]
                            A[i] = aux
                            break
                
                helper = A[i][i]
                if helper == 0:
                    print("WARNING! It's not possible to step the matrix. Error in row", i)
                    exit(1) 
                   
            else:
                helper = A[j][i]
                mult = helper / A[i][i]
                row1 = A[i]
                row2 = A[j]
                for k in range(0, len(row2)):
                    row2[k] -= (mult*row1[k])
                A[j] = row2
    
    return Ab  

def aumMatrix(A, b):
    cont = 0
    for i in A:
        i.append(b[cont])
        cont += 1
    return A

def clear(stepMat, n):
    vector = []
    for x in range(n):
        vector.append(0)
    vector[n-1]=stepMat[n-1][n]/stepMat[n-1][n-1]
    i = n-2
    while i >= 0:
        result = 0
        p = len(vector)-1
        while p >= 0:
            result += (stepMat[i][p]*vector[p])
            p -= 1
        vector[i] = (stepMat[i][n]-result)/stepMat[i][i]
        i -= 1
    return vector


name = input("Enter the name of the file you want the answer to be saved to. It's going to have a '.txt' extension: ")
matrix_rows = int(input("As this has to be a square matrix, the number of rows is going to be the same as the number of columns. \
                \nEnter the number of rows in the matrix: "))
matrix = []
vector = []
print("Enter the %s x %s matrix: "% (matrix_rows, matrix_rows))
print("Separate each number with a space and press ENTER to change the row ")
for j in range(matrix_rows):
        matrix.append(list(map(float, input().rstrip().split())))
print("Enter the vector. Separate each number with a space")
vector.append(list(map(float, input().rstrip().split())))
vector = vector[0]
print("You will find the result in " + name + ".txt")
matrix_aux = deepcopy(matrix)
vector_aux = copy(vector)
with open(name + ".txt", "w") as result:
    print("The stepped matrix is: ", file=result)
    B = stepped(matrix_aux, vector_aux)
    print(DataFrame(B), file=result)
    print("\n", file=result)
    A = clear(B, len(matrix))
    num = 1
    for x in A:
        print("x" + str(num) + " = " + str(x), file=result)
        num += 1
    print("\n", file=result)
    print("The inital matrix was:" , file=result)
    print(DataFrame(aumMatrix(matrix, vector)), file=result)
