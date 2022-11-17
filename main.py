from A01570748_M1.clean_model import CleanModel
import matplotlib.pyplot as plt
import time


def basic_example_space():
    print("Matriz Inicial (Sucia)")
    A = int(input("Ingresa la cantidad de agentes: "))
    N = int(input("Ingresa la cantidad de filas: "))
    M = int(input("Ingresa la cantidad de columnas: "))
    p = float(input("Ingresa el porcentaje (numero decimal 0.00 - 1.00) de celdas sucias: "))
    start_time = time.time()
    model = CleanModel(A, N, M, p)
    while model.celdas_suc != 0:
        model.step()
        print("\n")

    print("Matriz Final (Limpia)")
    print(model.dirty_matrix)
    print("--- %s segundos ---" % (time.time() - start_time))
