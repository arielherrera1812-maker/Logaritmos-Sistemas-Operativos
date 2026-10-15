def simular_prioridad():
    print("=" * 50)
    print("   SIMULADOR DE PLANIFICACIÓN - PRIORIDAD (No Apropiativo)")
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
        priority = int(input(f"Prioridad para {nombre} (menor número = mayor prioridad): "))
        
        procesos.append({
            'nombre': nombre,
            'burst': burst,
            'arrival': arrival,
            'priority': priority,
            'completed': False,
            'completion': 0,
            'waiting': 0,
            'turnaround': 0
        })

    tiempo_actual = 0
    completados = 0

    # Lógica del algoritmo de Prioridad No Apropiativo
    while completados < n:
        # Filtrar procesos que ya han llegado y aún no se han completado
        disponibles = [p for p in procesos if p['arrival'] <= tiempo_actual and not p['completed']]

        if not disponibles:
            # Si la CPU está libre pero ningún proceso ha llegado, avanzamos al siguiente tiempo de llegada
            no_completados = [p for p in procesos if not p['completed']]
            if no_completados:
                siguiente_llegada = min(p['arrival'] for p in no_completados)
                tiempo_actual = siguiente_llegada
            continue

        # Seleccionar el proceso con la mayor prioridad (menor número). 
        # En caso de empate en prioridad, se prioriza el que tenga menor tiempo de llegada (FIFO).
        p_actual = min(disponibles, key=lambda x: (x['priority'], x['arrival']))

        # Ejecutar el proceso
        inicio = tiempo_actual
        tiempo_actual += p_actual['burst']
        
        p_actual['completion'] = tiempo_actual
        p_actual['waiting'] = inicio - p_actual['arrival']
        p_actual['turnaround'] = p_actual['completion']
        p_actual['completed'] = True
        completados += 1

    # Cálculo de promedios (TEM y TRM)
    total_espera = sum(p['waiting'] for p in procesos)
    total_retorno = sum(p['turnaround'] for p in procesos)
    
    tem = total_espera / n
    trm = total_retorno / n

    # Ordenar para mostrar los resultados de forma ordenada por nombre
    procesos.sort(key=lambda x: x['nombre'])

    # Imprimir resultados limpios
    print("\n" + "=" * 50)
    print("                 RESULTADOS FINALES (PRIORIDAD)")
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
    simular_prioridad()