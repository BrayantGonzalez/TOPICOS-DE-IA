import random
import math
from typing import List, Tuple, Callable, Optional

class Particle:
    def __init__(self, dimensions: int, bounds: Tuple[float, float], objective_function: Callable[[List[float]], float]):
        """
        Inicializa una partícula con posición y velocidad aleatorias dentro de los límites especificados.
        
        Args:
            dimensions: Número de dimensiones del espacio de búsqueda.
            bounds: Tupla con (límite_inferior, límite_superior) para cada dimensión.
            objective_function: Función objetivo a optimizar.
        """
        if dimensions <= 0:
            raise ValueError("El número de dimensiones debe ser > 0")
        if bounds[0] >= bounds[1]:
            raise ValueError("El límite inferior debe ser < límite superior")
        
        self.dimensions = dimensions
        self.bounds = bounds
        self.objective_function = objective_function
        
        # Inicialización aleatoria dentro de los límites
        self.position = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
        self.velocity = [random.uniform(-(bounds[1]-bounds[0]), (bounds[1]-bounds[0])) for _ in range(dimensions)]
        
        # Memoria de la partícula (mejor posición y valor encontrado)
        self.best_position = self.position.copy()
        self.best_value = self.evaluate()
    
    def evaluate(self) -> float:
        """Evalúa la posición actual en la función objetivo."""
        return self.objective_function(self.position)
    
    def update_velocity(self, global_best_position: List[float], w: float = 0.5, c1: float = 1.5, c2: float = 1.5):
        """
        Actualiza la velocidad según las reglas del PSO.
        
        Args:
            global_best_position: Mejor posición encontrada por el enjambre.
            w: Factor de inercia (controla la influencia de la velocidad anterior).
            c1: Peso cognitivo (influencia del mejor histórico personal).
            c2: Peso social (influencia del mejor histórico global).
        """
        for i in range(self.dimensions):
            r1, r2 = random.random(), random.random()
            cognitive = c1 * r1 * (self.best_position[i] - self.position[i])
            social = c2 * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive + social
    
    def update_position(self):
        """Actualiza la posición y aplica los límites del espacio."""
        for i in range(self.dimensions):
            self.position[i] += self.velocity[i]
            
            # Aplicar límites con rebote amortiguado
            if self.position[i] < self.bounds[0]:
                self.position[i] = self.bounds[0]
                self.velocity[i] *= -0.5
            elif self.position[i] > self.bounds[1]:
                self.position[i] = self.bounds[1]
                self.velocity[i] *= -0.5
        
        # Actualizar memoria si hay mejora
        current_value = self.evaluate()
        if current_value < self.best_value:
            self.best_position = self.position.copy()
            self.best_value = current_value

class Swarm:
    def __init__(self, num_particles: int, dimensions: int, bounds: Tuple[float, float], 
                 objective_function: Callable[[List[float]], float], max_iter: int = 100):
        """
        Inicializa un enjambre de partículas para optimización.
        
        Args:
            num_particles: Número de partículas.
            dimensions: Dimensiones del espacio de búsqueda.
            bounds: Límites (inferior, superior) para cada dimensión.
            objective_function: Función a optimizar (minimizar).
            max_iter: Máximo de iteraciones.
        """
        self.num_particles = num_particles
        self.dimensions = dimensions
        self.bounds = bounds
        self.objective_function = objective_function
        self.max_iter = max_iter
        
        # Crear partículas
        self.particles = [Particle(dimensions, bounds, objective_function) for _ in range(num_particles)]
        
        # Inicializar mejor global
        self.global_best_position = self.particles[0].best_position.copy()
        self.global_best_value = self.particles[0].best_value
        self._update_global_best()
    
    def _update_global_best(self):
        """Actualiza la mejor posición global del enjambre."""
        for particle in self.particles:
            if particle.best_value < self.global_best_value:
                self.global_best_position = particle.best_position.copy()
                self.global_best_value = particle.best_value
    
    def optimize(self, w: float = 0.5, c1: float = 1.5, c2: float = 1.5, 
                 early_stopping: Optional[int] = None, verbose: bool = False) -> Tuple[List[float], float]:
        """
        Ejecuta el algoritmo PSO.
        
        Args:
            w: Factor de inercia.
            c1: Peso cognitivo.
            c2: Peso social.
            early_stopping: Iteraciones sin mejora para parar.
            verbose: Mostrar progreso.
            
        Returns:
            (mejor_posición, mejor_valor)
        """
        best_iteration = 0
        no_improvement = 0
        
        for iteration in range(self.max_iter):
            # Actualizar todas las partículas
            for particle in self.particles:
                particle.update_velocity(self.global_best_position, w, c1, c2)
                particle.update_position()
            
            # Actualizar mejor global
            previous_best = self.global_best_value
            self._update_global_best()
            
            # Verificar mejora
            if self.global_best_value < previous_best:
                best_iteration = iteration
                no_improvement = 0
            else:
                no_improvement += 1
            
            # Mostrar progreso
            if verbose and iteration % 10 == 0:
                print(f"Iter {iteration}: Mejor valor = {self.global_best_value:.6f}")
            
            # Parada temprana
            if early_stopping and no_improvement >= early_stopping:
                if verbose:
                    print(f"Parada temprana en iter {iteration} (sin mejora por {early_stopping} iteraciones)")
                break
        
        if verbose:
            print(f"\nOptimización completada en {best_iteration+1} iteraciones")
            print(f"Mejor posición: {self.global_best_position}")
            print(f"Mejor valor: {self.global_best_value:.6f}")
        
        return self.global_best_position, self.global_best_value

# Función de prueba (mínimo en 0)
def sphere_function(x: List[float]) -> float:
    return sum(xi**2 for xi in x)

# Función de prueba más compleja (múltiples mínimos)
def rastrigin_function(x: List[float]) -> float:
    A = 10
    return A * len(x) + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)

if __name__ == "__main__":
    print("=== Optimización con Enjambre de Partículas ===")
    
    # Configuración
    num_particles = 30
    dimensions = 3
    bounds = (-5.0, 5.0)
    max_iterations = 100
    
    # Seleccionar función objetivo
    objective_func = sphere_function  # Cambiar a rastrigin_function para prueba más compleja
    
    # Crear enjambre
    swarm = Swarm(num_particles, dimensions, bounds, objective_func, max_iterations)
    
    # Ejecutar optimización
    print("\nIniciando optimización...")
    best_pos, best_val = swarm.optimize(
        w=0.7,          # Factor de inercia
        c1=1.5,         # Peso cognitivo
        c2=2.0,         # Peso social
        early_stopping=20,  # Parar si no hay mejora en 20 iteraciones
        verbose=True     # Mostrar progreso
    )
    
    print("\nResultado final:")
    print(f"Mejor solución encontrada: {best_pos}")
    print(f"Valor de la función objetivo: {best_val:.6f}")