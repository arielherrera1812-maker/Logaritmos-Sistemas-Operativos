def simular_fifo():
    print("=" * 50)
    print("   SIMULADOR DE PLANIFICACIÓN DE CPU - ALGORITMO FIFO")
    print("=" * 50)
    
    try:
        n = int(input("Ingrese el número total de trabajos/procesos: "))
    except ValueError:
        print("Por favor, ingrese un número entero válido.")
        return

    procesos = []

    # Captura de datos ingresados por el usuario
    for i in range(n):
        print(f"\n--- Trabajo {i + 1} ---")
        nombre = input("Nombre del trabajo (ej. A, B, C): ").strip().upper()
        burst = int(input(f"Ráfaga de CPU para {nombre}: "))
        arrival = int(input(f"Tiempo de llegada para {nombre}: "))
        
        procesos.append({
            'nombre': nombre,
            'burst': burst,
            'arrival': arrival,
            'completion': 0,
            'waiting': 0,
            'turnaround': 0
        })

    # 1. Ordenar por Tiempo de Llegada (FIFO: el primero en llegar es el primero en ser atendido)
    procesos.sort(key=lambda x: x['arrival'])

    tiempo_actual = 0
    for p in procesos:
        # Si la CPU está libre y el proceso aún no llega, el tiempo avanza hasta su llegada
        if tiempo_actual < p['arrival']:
            tiempo_actual = p['arrival']

        # Tiempo de finalización (equivalente al tiempo de retorno según el ejercicio del profe)
        tiempo_actual += p['burst']
        p['completion'] = tiempo_actual

        # Tiempo de espera = Tiempo de inicio - Tiempo de llegada
        # (El tiempo de inicio es completion - burst)
        inicio = p['completion'] - p['burst']
        p['waiting'] = inicio - p['arrival']

        # Tiempo de retorno (Tiempo de finalización total desde t=0)
        p['turnaround'] = p['completion']

    # 2. Calcular los promedios (TEM y TRM)
    total_espera = sum(p['waiting'] for p in procesos)
    total_retorno = sum(p['turnaround'] for p in procesos)
    
    tem = total_espera / n
    trm = total_retorno / n

    # 3. Imprimir resultados limpios
    print("\n" + "=" * 50)
    print("                 RESULTADOS FINALES")
    print("=" * 50)
    
    for p in procesos:
        print(f"Trabajo {p['nombre']}:")
        print(f"  • Tiempo de Espera   = {p['waiting']}")
        print(f"  • Tiempo de Retorno  = {p['turnaround']}")
        print("-" * 30)

    print("\n" + "=" * 50)
    print(f" Tiempo Medio de Espera (TEM)       = {tem:.2f} ut")
    print(f" Tiempo de Retorno Medio (TRM)      = {trm:.2f} ut")
    print("=" * 50)

if __name__ == "__main__":
    simular_fifo()