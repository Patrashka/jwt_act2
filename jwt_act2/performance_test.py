#!/usr/bin/env python3
"""
Script de prueba de rendimiento para comparar SQL vs Redis
"""

import requests
import json
import time
import statistics
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "username": "admin",
    "password": "admin123"
}

def make_request(endpoint, method="POST", data=None, headers=None):
    """Hacer una petición HTTP y medir el tiempo"""
    url = f"{BASE_URL}{endpoint}"
    start_time = time.time()
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # en milisegundos
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        return {
            "success": False,
            "error": str(e),
            "response_time_ms": response_time,
            "data": None
        }

def test_login_performance(endpoint, num_tests=10):
    """Probar rendimiento de login"""
    print(f"\n🧪 Probando {endpoint} ({num_tests} pruebas)...")
    
    times = []
    successes = 0
    
    for i in range(num_tests):
        result = make_request(endpoint, data=TEST_USER)
        times.append(result["response_time_ms"])
        
        if result["success"]:
            successes += 1
            print(f"  ✅ Prueba {i+1}: {result['response_time_ms']:.2f}ms")
        else:
            print(f"  ❌ Prueba {i+1}: Error - {result.get('error', 'Unknown error')}")
    
    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        median_time = statistics.median(times)
        
        print(f"\n📊 Resultados de {endpoint}:")
        print(f"  ✅ Éxitos: {successes}/{num_tests}")
        print(f"  ⏱️  Tiempo promedio: {avg_time:.2f}ms")
        print(f"  ⚡ Tiempo mínimo: {min_time:.2f}ms")
        print(f"  🐌 Tiempo máximo: {max_time:.2f}ms")
        print(f"  📈 Tiempo mediano: {median_time:.2f}ms")
        
        return {
            "endpoint": endpoint,
            "successes": successes,
            "total_tests": num_tests,
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "median_time": median_time,
            "times": times
        }
    
    return None

def test_health_check():
    """Probar health check"""
    print("\n🏥 Verificando estado de la aplicación...")
    
    result = make_request("/api/health", method="GET")
    
    if result["success"]:
        data = result["data"]
        print(f"  ✅ Estado: {data.get('status', 'unknown')}")
        print(f"  🗄️  Base de datos: {data.get('database', 'unknown')}")
        print(f"  🔴 Redis: {data.get('redis', 'unknown')}")
        return True
    else:
        print(f"  ❌ Error en health check: {result.get('error', 'Unknown error')}")
        return False

def test_performance_comparison():
    """Probar endpoint de comparación de rendimiento"""
    print("\n⚡ Probando comparación de rendimiento...")
    
    result = make_request("/api/performance/compare", data=TEST_USER)
    
    if result["success"]:
        data = result["data"]
        comparison = data.get("comparison", {})
        analysis = data.get("performance_analysis", {})
        
        print(f"  📊 SQL: {comparison.get('sql', {}).get('response_time_ms', 0):.2f}ms")
        print(f"  🔴 Redis: {comparison.get('redis', {}).get('response_time_ms', 0):.2f}ms")
        print(f"  🏆 Sistema más rápido: {analysis.get('faster_system', 'unknown')}")
        print(f"  📈 Diferencia: {analysis.get('redis_advantage', 'unknown')}")
        
        return data
    else:
        print(f"  ❌ Error en comparación: {result.get('error', 'Unknown error')}")
        return None

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de rendimiento JWT SQL vs Redis")
    print("=" * 60)
    
    # Verificar que la aplicación esté funcionando
    if not test_health_check():
        print("\n❌ La aplicación no está funcionando correctamente")
        return
    
    # Probar rendimiento de login SQL
    sql_results = test_login_performance("/api/login", 5)
    
    # Probar rendimiento de login Redis
    redis_results = test_login_performance("/api-redis/login", 5)
    
    # Probar comparación directa
    comparison_results = test_performance_comparison()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL")
    print("=" * 60)
    
    if sql_results and redis_results:
        sql_avg = sql_results["avg_time"]
        redis_avg = redis_results["avg_time"]
        difference = redis_avg - sql_avg
        percentage = (difference / sql_avg * 100) if sql_avg > 0 else 0
        
        print(f"🗄️  SQL promedio: {sql_avg:.2f}ms")
        print(f"🔴 Redis promedio: {redis_avg:.2f}ms")
        print(f"📊 Diferencia: {difference:+.2f}ms ({percentage:+.1f}%)")
        
        if redis_avg < sql_avg:
            print(f"🏆 Redis es {abs(percentage):.1f}% más rápido que SQL")
        else:
            print(f"🏆 SQL es {abs(percentage):.1f}% más rápido que Redis")
    
    if comparison_results:
        print(f"\n⚡ Comparación directa:")
        analysis = comparison_results.get("performance_analysis", {})
        print(f"  {analysis.get('redis_advantage', 'No disponible')}")
    
    print(f"\n⏰ Pruebas completadas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
