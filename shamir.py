import random


def generateCoefficientsForPolynomialWithSecret(secretValue, threshold):
    coefficients = {0: secretValue}
    for index in range(1, threshold):
        coefficients[index] = random.randint(1, 256)
    return coefficients


def evaluatePolynomialAtX(valueOfX, coefficients):
    result = 0
    for exponent in coefficients:
        result += coefficients[exponent] * (valueOfX**exponent)
    return result


def createPartAtX(valueOfX, coefficients):
    return evaluatePolynomialAtX(valueOfX, coefficients)


def performLagrangeInterpolationAtX(valueOfX, partsX, partsY):
    total = 0
    for indexI in range(len(partsX)):
        numerator = 1
        denominator = 1
        for indexJ in range(len(partsX)):
            if indexI != indexJ:
                numerator *= valueOfX - partsX[indexJ]
                denominator *= partsX[indexI] - partsX[indexJ]
        total += partsY[indexI] * numerator // denominator
    return total


def reconstructSecretFromSelectedParts(selectedParts):
    partsX = [part[0] for part in selectedParts]
    partsY = [part[1] for part in selectedParts]
    return performLagrangeInterpolationAtX(0, partsX, partsY)


def menu():
    definedThreshold = None
    totalParts = None

    while True:
        print(" ------- SHAMIR SECRET ------- ")
        print("    [1] Generar                ")
        print("    [2] Reconstruir secreto    ")
        print("    [3] Salir                  ")
        print(" -------------- -------------- ")
        try:
            opcion = int(input("    Opción: "))
        except ValueError:
            print("     Error, ingrese un número válido")
            continue
        print(" -------------- -------------- ")

        if opcion == 1:
            try:
                print("\n         ------ GENERAR ------ ")
                secretValue = int(input("         Secreto           : "))
                totalParts = int(input("         Total de partes   : "))
                threshold = int(input("         Partes necesarias : "))
                if threshold > totalParts:
                    print(
                        "     Error, el umbral no puede ser mayor que el total de partes"
                    )
                    continue

                definedThreshold = threshold
            except ValueError:
                print("     Error, ingrese valores numéricos válidos")
                continue

            coefficients = generateCoefficientsForPolynomialWithSecret(
                secretValue, threshold
            )
            parts = []

            for partIndex in range(1, totalParts + 1):
                partValue = createPartAtX(partIndex, coefficients)
                parts.append((partIndex, partValue))

            print("         ------- PARTES ------ ")
            for part in parts:
                print(f"              Parte {part[0]}: ({part[0]},  {part[1]})")
            print("         ---------- ---------- ")

        elif opcion == 2:
            if definedThreshold is None or totalParts is None:
                print("     Error, primero debe generar un secreto y partes")
                continue

            try:
                print("\n         ---- Reconstruir ---- ")
                numPartsToUse = int(input("             Umbral              : "))
                if numPartsToUse < definedThreshold:
                    print(
                        f"  Error, se necesitan al menos {definedThreshold} partes para reconstruir el secreto"
                    )
                    continue
                if numPartsToUse > totalParts:
                    print(
                        f"  Error, no puede ingresar más partes ({numPartsToUse}) que las definidas ({totalParts})"
                    )
                    continue

                selectedParts = []
                for i in range(numPartsToUse):
                    partIndex = int(input(f"             Indice parte ({i + 1})   : "))
                    partValue = int(input(f"             Valor parte  ({i + 1})   : "))
                    selectedParts.append((partIndex, partValue))

                recoveredSecret = reconstructSecretFromSelectedParts(selectedParts)
                print("             Secreto recuperado: ", recoveredSecret)
                print("         -------------- -------------- ")

            except ValueError as e:
                print(f"  Error, ingrese un valor numérico")
                continue

        elif opcion == 3:
            print("  Hasta luego...")
            break
        else:
            print("  Ingrese una opción válida...")
            print(" -------------- -------------- ")


menu()
