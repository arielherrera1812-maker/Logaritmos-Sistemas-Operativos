def simular_round_robin():
    print("=" * 50)
    print("   SIMULADOR DE PLANIFICACIÓN - ROUND ROBIN")
    print("=" * 50)
    
    try:
        n = int(input("Ingrese el número total de trabajos/procesos: "))
        quantum = int(input("Ingrese el valor del Quantum (q): "))
    except ValueError:
        print("Por favor, ingrese números enteros válidos.")
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
            'burst_original': burst,
            'remaining': burst,
            'arrival': arrival,
            'completion': 0,
            'waiting': 0,
            'turnaround': 0
        })

    # Ordenar copias para manejar el orden de llegada correctamente
    procesos_ordenados_llegada = sorted(procesos, key=lambda x: x['arrival'])
    
    tiempo_actual = 0
    cola = []
    completados = 0
    i_llegada = 0
    
    # Cargar los procesos que llegan en el tiempo inicial (t = 0 o el menor tiempo)
    while i_llegada < n and procesos_ordenados_llegada[i_llegada]['arrival'] <= tiempo_actual:
        cola.append(procesos_ordenados_llegada[i_llegada])
        i_llegada += 1

    # Si en t=0 no hay procesos, avanzamos al tiempo del primer proceso en llegar
    if not cola and i_llegada < n:
        tiempo_actual = procesos_ordenados_llegada[i_llegada]['arrival']
        while i_llegada < n and procesos_ordenados_llegada[i_llegada]['arrival'] <= tiempo_actual:
            cola.append(procesos_ordenados_llegada[i_llegada])
            i_llegada += 1

    # Bucle principal de Round Robin
    while completados < n:
        if not cola:
            tiempo_actual = procesos_ordenados_llegada[i_llegada]['arrival']
            while i_llegada < n and procesos_ordenados_llegada[i_llegada]['arrival'] <= tiempo_actual:
                if procesos_ordenados_llegada[i_llegada] not in cola:
                    cola.append(procesos_ordenados_llegada[i_llegada])
                i_llegada += 1

        p = cola.pop(0)

        # Determinar cuánto tiempo va a correr este turno (el quantum o lo que le falte)
        tiempo_ejecucion = min(quantum, p['remaining'])
        tiempo_actual += tiempo_ejecucion
        p['remaining'] -= tiempo_ejecucion

        # Agregar a la cola los nuevos procesos que hayan llegado *durante* este intervalo de tiempo
        while i_llegada < n and procesos_ordenados_llegada[i_llegada]['arrival'] <= tiempo_actual:
            if procesos_ordenados_llegada[i_llegada] not in cola and procesos_ordenados_llegada[i_llegada]['remaining'] > 0:
                cola.append(procesos_ordenados_llegada[i_llegada])
            i_llegada += 1

        # Si el proceso todavía tiene ráfaga pendiente, vuelve al final de la cola
        if p['remaining'] > 0:
            cola.append(p)
        else:
            # El proceso ha finalizado
            p['completion'] = tiempo_actual
            # Tiempo de Retorno = Tiempo de Finalización - Tiempo de Llegada
            p['turnaround'] = p['completion'] - p['arrival']
            # Tiempo de Espera = Tiempo de Retorno - Ráfaga Original de CPU
            p['waiting'] = p['turnaround'] - p['burst_original']
            completados += 1

    # Cálculo de promedios (TEM y TRM)
    total_espera = sum(p['waiting'] for p in procesos)
    total_retorno = sum(p['turnaround'] for p in procesos)
    
    tem = total_espera / n
    trm = total_retorno / n

    # Ordenar alfabéticamente para presentar los resultados ordenados
    procesos.sort(key=lambda x: x['nombre'])

    # Imprimir resultados limpios
    print("\n" + "=" * 50)
    print("               RESULTADOS FINALES (ROUND ROBIN)")
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
    simular_round_robin()