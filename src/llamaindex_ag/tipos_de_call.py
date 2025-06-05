import asyncio
import time

# ========== EJEMPLO SIMPLE PARA PRINCIPIANTES ==========


def simulate_api_call(query: str, delay: float = 2.0) -> str:
    """
    Simula una llamada a una API que toma tiempo.
    En la vida real esto podría ser: consulta a DB, API externa, etc.
    """
    print(f"🔄 Procesando: '{query}'...")
    time.sleep(delay)  # Simula que la operación toma tiempo
    return f"✅ Respuesta para: '{query}'"


async def simulate_async_api_call(query: str, delay: float = 2.0) -> str:
    """
    Versión asíncrona - no bloquea mientras espera
    """
    print(f"🚀 Procesando async: '{query}'...")
    await asyncio.sleep(delay)  # Versión async de time.sleep()
    return f"✅ Respuesta async para: '{query}'"


# ========== EJEMPLOS DE USO ==========


def ejemplo_sincrono():
    """
    MODO SÍNCRONO: Una tarea después de otra
    Como hacer cola en el banco - esperas tu turno
    """
    print("\n🐌 === EJEMPLO SÍNCRONO (LENTO) ===")
    start_time = time.time()

    # Hacemos 3 "consultas" una después de otra
    queries = ["¿Qué es Python?", "¿Qué es async?", "¿Qué es await?"]

    results = []
    for i, query in enumerate(queries, 1):
        print(f"📞 Consulta {i}/3:")
        result = simulate_api_call(query, delay=1.5)
        results.append(result)
        print(f"   {result}")

    total_time = time.time() - start_time
    print(f"\n⏱️ Tiempo total SÍNCRONO: {total_time:.1f} segundos")
    return results


async def ejemplo_asincrono():
    """
    MODO ASÍNCRONO: Todas las tareas en paralelo
    Como tener 3 cajeros en el banco - todos atienden a la vez
    """
    print("\n🚀 === EJEMPLO ASÍNCRONO (RÁPIDO) ===")
    start_time = time.time()

    queries = ["¿Qué es Python?", "¿Qué es async?", "¿Qué es await?"]

    print("🔄 Iniciando 3 consultas EN PARALELO...")

    # Crear todas las tareas
    tasks = [simulate_async_api_call(query, delay=1.5) for query in queries]

    # Ejecutar todas al mismo tiempo
    results = await asyncio.gather(*tasks)

    # Mostrar resultados
    for i, result in enumerate(results, 1):
        print(f"   📋 Resultado {i}: {result}")

    total_time = time.time() - start_time
    print(f"\n⚡ Tiempo total ASÍNCRONO: {total_time:.1f} segundos")
    return results


def comparar_enfoques():
    """Compara ambos enfoques lado a lado"""
    print("🆚 === COMPARACIÓN DIRECTA ===\n")

    # Medir tiempo síncrono
    print("🔵 Probando enfoque SÍNCRONO...")
    sync_start = time.time()
    ejemplo_sincrono()
    sync_time = time.time() - sync_start

    print("\n" + "=" * 50)

    # Medir tiempo asíncrono
    print("🟢 Probando enfoque ASÍNCRONO...")
    async_start = time.time()
    asyncio.run(ejemplo_asincrono())
    async_time = time.time() - async_start

    # Mostrar comparación
    print("\n📊 === RESULTADOS FINALES ===")
    print(f"🐌 Síncrono:   {sync_time:.1f} segundos")
    print(f"🚀 Asíncrono:  {async_time:.1f} segundos")

    mejora = ((sync_time - async_time) / sync_time) * 100
    print(f"⚡ Mejora:     {mejora:.0f}% más rápido!")


# ========== CONCEPTOS CLAVE ==========


def explicar_conceptos():
    """Explica los conceptos básicos"""
    print(
        """
🎓 === CONCEPTOS BÁSICOS ===

🔵 SÍNCRONO (call):
   • Una tarea después de otra
   • Bloquea hasta completarse
   • Más fácil de entender
   • Más lento con múltiples tareas

🟢 ASÍNCRONO (acall):
   • Múltiples tareas al mismo tiempo
   • No bloquea - puede hacer otras cosas
   • Más complejo de entender
   • Mucho más rápido con múltiples tareas

💡 ANALOGÍA:
   Síncrono  = Un chef cocinando platos uno por uno
   Asíncrono = Tres chefs cocinando platos al mismo tiempo

🎯 ¿CUÁNDO USAR QUÉ?
   • Una sola tarea    → Síncrono
   • Múltiples tareas  → Asíncrono
   • Scripts simples   → Síncrono
   • Apps web/APIs     → Asíncrono
    """
    )


# ========== EJEMPLOS EXTRA SIMPLES ==========


async def ejemplo_super_simple():
    """Ejemplo súper básico para entender async/await"""
    print("\n🔰 === EJEMPLO SÚPER SIMPLE ===")

    print("1️⃣ Inicio")

    print("2️⃣ Iniciando tarea que toma 2 segundos...")
    result = await simulate_async_api_call("Hola mundo", delay=2.0)

    print("3️⃣ ¡Tarea completada!")
    print(f"4️⃣ Resultado: {result}")


if __name__ == "__main__":
    print("🎉 DEMO: Síncrono vs Asíncrono - Para Principiantes\n")

    # Explicar conceptos primero
    explicar_conceptos()

    # Ejemplo súper simple
    asyncio.run(ejemplo_super_simple())

    # Comparación completa
    comparar_enfoques()

    print("\n🎯 ¡Ahora ya sabes la diferencia entre síncrono y asíncrono!")
