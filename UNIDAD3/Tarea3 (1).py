import random
import math
from typing import List, Tuple, Callable, Optional

class Particle:
    def __init__(self, dimensions: int, bounds: Tuple[float, float], objective_function: Callable[[List[float]], float]):
        if dimensions <= 0:
            raise ValueError("El número de dimensiones debe ser > 0")
        if bounds[0] >= bounds[1]:
            raise ValueError("El límite inferior debe ser < límite superior")
        
        self.dimensions = dimensions
        self.bounds = bounds
        self.objective_function = objective_function
        
        self.position = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
        self.velocity = [random.uniform(-(bounds[1]-bounds[0]), (bounds[1]-bounds[0])) for _ in range(dimensions)]
        
        self.best_position = self.position.copy()
        self.best_value = self.evaluate()
    
    def evaluate(self) -> float:
        return self.objective_function(self.position)
    
    def update_velocity(self, global_best_position: List[float], w: float = 0.5, c1: float = 1.5, c2: float = 1.5):
        for i in range(self.dimensions):
            r1, r2 = random.random(), random.random()
            cognitive = c1 * r1 * (self.best_position[i] - self.position[i])
            social = c2 * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive + social
    
    def update_position(self):
        for i in range(self.dimensions):
            self.position[i] += self.velocity[i]
            if self.position[i] < self.bounds[0]:
                self.position[i] = self.bounds[0]
                self.velocity[i] *= -0.5
            elif self.position[i] > self.bounds[1]:
                self.position[i] = self.bounds[1]
                self.velocity[i] *= -0.5
        
        current_value = self.evaluate()
        if current_value < self.best_value:
            self.best_position = self.position.copy()
            self.best_value = current_value

class Swarm:
    def __init__(self, num_particles: int, dimensions: int, bounds: Tuple[float, float], 
                 objective_function: Callable[[List[float]], float], max_iter: int = 100):
        self.num_particles = num_particles
        self.dimensions = dimensions
        self.bounds = bounds
        self.objective_function = objective_function
        self.max_iter = max_iter
        
        self.particles = [Particle(dimensions, bounds, objective_function) for _ in range(num_particles)]
        self.global_best_position = self.particles[0].best_position.copy()
        self.global_best_value = self.particles[0].best_value
        self._update_global_best()
    
    def _update_global_best(self):
        for particle in self.particles:
            if particle.best_value < self.global_best_value:
                self.global_best_position = particle.best_position.copy()
                self.global_best_value = particle.best_value
    
    def optimize(self, w: float = 0.5, c1: float = 1.5, c2: float = 1.5, 
                 early_stopping: Optional[int] = None, verbose: bool = False) -> Tuple[List[float], float]:
        best_iteration = 0
        no_improvement = 0
        
        for iteration in range(self.max_iter):
            for particle in self.particles:
                particle.update_velocity(self.global_best_position, w, c1, c2)
                particle.update_position()
            
            previous_best = self.global_best_value
            self._update_global_best()
            
            if self.global_best_value < previous_best:
                best_iteration = iteration
                no_improvement = 0
            else:
                no_improvement += 1
            
            if verbose and iteration % 10 == 0:
                print(f"Iter {iteration}: Mejor valor = {self.global_best_value:.6f}")
            
            if early_stopping and no_improvement >= early_stopping:
                if verbose:
                    print(f"Parada temprana en iter {iteration} (sin mejora por {early_stopping} iteraciones)")
                break
        
        if verbose:
            print(f"\nOptimización completada en {best_iteration+1} iteraciones")
            print(f"Mejor posición: {self.global_best_position}")
            print(f"Mejor valor: {self.global_best_value:.6f}")
        
        return self.global_best_position, self.global_best_value

# === FUNCIONES ADICIONALES SOLICITADAS ===

def mover_particula(particle: Particle, global_best_position: List[float], w: float, c1: float, c2: float):
    particle.update_velocity(global_best_position, w, c1, c2)
    particle.update_position()

def evaluar_particula(particle: Particle) -> float:
    return particle.evaluate()

def mover_enjambre(particles: List[Particle], global_best_position: List[float], w: float, c1: float, c2: float):
    for particle in particles:
        mover_particula(particle, global_best_position, w, c1, c2)

def evaluar_enjambre(particles: List[Particle]) -> List[float]:
    return [evaluar_particula(p) for p in particles]

# === FUNCIONES OBJETIVO ===

def sphere_function(x: List[float]) -> float:
    return sum(xi**2 for xi in x)

def rastrigin_function(x: List[float]) -> float:
    A = 10
    return A * len(x) + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)

# === EJECUCIÓN PRINCIPAL ===

if __name__ == "__main__":
    print("=== Optimización con Enjambre de Partículas ===")
    
    num_particles = 30
    dimensions = 3
    bounds = (-5.0, 5.0)
    max_iterations = 100
    
    objective_func = sphere_function  # Cambiar a rastrigin_function para prueba más compleja
    
    swarm = Swarm(num_particles, dimensions, bounds, objective_func, max_iterations)
    
    print("\nIniciando optimización...")
    best_pos, best_val = swarm.optimize(
        w=0.7,
        c1=1.5,
        c2=2.0,
        early_stopping=20,
        verbose=True
    )
    
    print("\nResultado final:")
    print(f"Mejor solución encontrada: {best_pos}")
    print(f"Valor de la función objetivo: {best_val:.6f}")
