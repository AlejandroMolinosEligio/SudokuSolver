sudoku = [6, 8, 0, 1, 3, 2, 4, 7, 0, 7, 0, 4, 0, 9, 8, 0, 0, 2, 0, 1, 9, 0, 6, 0, 5, 0, 0, 8, 0, 1, 3, 0, 0, 7, 0, 0, 0, 0, 0, 8, 0, 0, 3, 4, 5, 4, 7, 0, 2, 0, 0, 0, 0, 0, 0, 0, 7, 0, 8, 3, 0, 0, 4, 0, 0, 0, 0, 0, 5, 6, 0, 0, 0, 6, 0, 4, 2, 7, 0, 1, 0]


def print_sudoku(puzzle):

    def format_cell(cell):
        """ Convierte cada celda a una cadena con longitud fija """
        if isinstance(cell, list):  # Si es una lista de posibilidades
            return f"{','.join(map(str, cell)):^10}"  # Centrado en 9 caracteres
        return f"{cell:^10}"  # Un solo número, también centrado en 9 caracteres

    for i in range(9):
        row = [format_cell(puzzle[j]) for j in range(i * 9, (i + 1) * 9)]
        row = [''.join(row[i:i+3]) for i in range(0, len(row), 3)]
        print(" | ".join(row))  # Separación por bloques
        if i in [2, 5]:  # Línea divisoria tras cada subcuadrante de 3x3
            print("-" * len(" | ".join(row)))

def possibilities(puzzle):

    dicc = dict()

    for i, number in enumerate(puzzle):

        if number != 0: dicc[(i//9, i%9)] = [number]
        else:
            dicc[(i//9, i%9)] = [1,2,3,4,5,6,7,8,9]

    iteration = 1
    while True:
        
        print(f'[*] Iteración {iteration}:\n')
        iteration +=1
        diccAux = {key: dicc[key].copy() for key in dicc}
        for row, col in dicc:
        
            if len(diccAux[(row,col)]) != 1:
                poss = check_row(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss
                poss = check_column(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss
                poss = check_matrix(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss
                poss = check_matrixUnique(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss

        print_dict(dicc)
        if dicc == diccAux: break
        dicc = diccAux.copy()

    print_sudoku([dicc[key] if len(dicc[key])!= 1 else dicc[key][0] for key in dicc])

    if all([len(dicc[i])==1 for i in dicc]):
        return None

    print(f'\n[*] Probando soluciones avanzadas...\n')
    diccAux = {key: dicc[key].copy() for key in dicc}
    dicc = tryPossibilities([diccAux], puzzle)
    print(f'\n[+] SOLUCIÓN FINAL:\n')
    print_sudoku([dicc[key] if len(dicc[key])!= 1 else dicc[key][0] for key in dicc])

def print_dict(dicc):

    rowO = None
    colO = None
    for row in range(0, 9, 3):
        for col in range(0,9, 3):
            for row2 in range(row, row+3):
                for col2 in range(col, col+3):
                    print(f'{(row2, col2)} = {dicc[(row2, col2)]}')
            print(f'\n')

def check_column(row, col ,poss, puzzle, dicc):
    
    poss = dicc[(row, col)]
    if len(poss) == 1: return poss
    if len(poss) == 1:
        if any([poss[0] == dicc[(i,col)][0] for i in range(0,9) if i!= row and len(dicc[(i,col)])==1]):
            return []
        return poss

    for j in range(0,9):
        if j == row: continue
        possAux = dicc[(j,col)]
        if len(possAux) == 1 and possAux[0] in poss:
            poss.remove(possAux[0])

    return poss

def check_row(row, col ,poss, puzzle, dicc):

    poss = dicc[(row, col)]
    if len(poss) == 1: 
        if any([poss[0] == dicc[(row,i)][0] for i in range(0,9) if i!= col and len(dicc[(row,i)])==1]):
            return []
        return poss

    for i in range(0,9):
        if i == col: continue
        possAux = dicc[(row,i)] 
        if len(possAux) == 1 and possAux[0] in poss:
            poss.remove(possAux[0])

    return poss

def check_matrix(row, col ,poss, puzzle, dicc):
   
    row_min = (row // 3) * 3
    row_max = row_min + 3

    col_min = (col // 3) * 3
    col_max = col_min + 3

    poss = dicc[(row, col)]

    if len(poss) == 1:
        for i in range(row_min, row_max):
            for j in range(col_min, col_max):
                if i == row and j == col: continue
                possAux = dicc[(i,j)]
                if len(possAux) == 1 and possAux[0] == poss[0]:
                    return []
        return poss
    
    for i in range(row_min, row_max):
        for j in range(col_min, col_max):
            if i == row and j == col: continue
            possAux = dicc[(i,j)]
            if len(possAux) == 1 and possAux[0] in poss:
                poss.remove(possAux[0])
    
    return poss

def check_matrixUnique(row, col ,poss, puzzle, dicc):

    row_min = (row // 3) * 3
    row_max = row_min + 3

    col_min = (col // 3) * 3
    col_max = col_min + 3

    poss = dicc[(row, col)]

    if len(poss) == 1:
        return poss

    for number in poss:
        check = True
        for i in range(row_min, row_max):
            for j in range(col_min, col_max):
                if i == row and j == col: continue
                possAux = dicc[(i,j)]
                if number in possAux:
                    check = False
                    break
            if not check:
                break

        if check: poss = [number]

    return poss

def tryPossibilities(diccList, puzzle):

    while not all([len(diccList[-1][i])==1 for i in diccList[-1]]):
        print(f'[*] Estado de la solución {len(diccList)}...\n')
        diccAux = diccList[-1]
        print_sudoku([diccAux[key][0] if len(diccAux[key])==1 else diccAux[key] for key in diccAux])
        print('\n')
        for key in diccAux:
            check = True
            options = diccAux[key]
            if len(options) > 1:
                solutions = []
                for option in options:
                    newDicc = {key: diccAux[key] for key in diccAux}
                    newDicc[key] = [option]
                    print(f'[Info] Option: {option} de {options} - INDEX: {key}')
                    solution = iterations(newDicc, puzzle)
                    if solution == None:
                        print(f'[!] SIN SOLUCIÓN!')
                        continue
                    elif type(solution) == dict:
                        print(f'[*] POSIBLE SOLUCIÓN')
                        check = False
                        diccList.append(solution)
                        solution = tryPossibilities(diccList, puzzle)
                        solutions.append(solution == None)
                        if solution == None:
                            diccList.pop()
                            print(f'\n[!] SIN SOLUCIÓN FINAL. Volviendo a dicc {len(diccList)}\n')
                            print_sudoku([diccAux[key][0] if len(diccList[-1][key])==1 else diccList[-1][key] for key in diccList[-1]])
                        if isinstance(solution, dict):
                            return solution
                if all(solutions):
                    print(f'[!] Ninguna opción válida para {options} - INDEX: {key}')
                    return None
                if check: return None
            else:
                continue

    
    return diccList[-1]
        
def iterations(dicc, puzzle):

    iteration = 1
    while True:

        iteration +=1
        diccAux = {key: dicc[key].copy() for key in dicc}
        rowN = 0

        for row, col in dicc:

            if len(diccAux[(row,col)]) != 1:
                poss = check_row(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss
                poss = check_column(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss
                poss = check_matrix(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss
                poss = check_matrixUnique(row, col, diccAux[(row, col)], puzzle, diccAux)
                diccAux[(row, col)] = poss
        if any(len(dicc[i])==0 for i in dicc): 
            return None
        if dicc == diccAux: break
        dicc = diccAux.copy()
    
    if any([len(dicc[i])==0 for i in dicc]):
        return None
    return dicc

if __name__ == '__main__':

    sudokuAux = input('Mete el sudoku separado por comas: ')
    if sudokuAux != '':
        sudokuAux = [int(i) for i in sudokuAux.split(',')]
        if len(sudokuAux) != 81: print(f'[!] Tamaño del sudoku no válido')
        else:
            sudoku = sudokuAux

    print('\n')
    print_sudoku(sudoku)
    print('\n')
    possibilities(sudoku)
