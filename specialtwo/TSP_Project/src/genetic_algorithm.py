import numpy as np
from utils import calculate_route_distance, generate_random_route
import time

class GeneticAlgorithmTSP:
    """
    Genetik Algoritma ile TSP çözümü
    """
    
    def __init__(self, distance_matrix, population_size=100, 
                 generations=500, mutation_rate=0.01, 
                 crossover_rate=0.9, start_city=0):
        """
        Args:
            distance_matrix: Şehirler arası mesafe matrisi
            population_size: Popülasyon büyüklüğü
            generations: Maksimum nesil sayısı
            mutation_rate: Mutasyon oranı (0.01 = %1)
            crossover_rate: Çaprazlama oranı (0.9 = %90)
            start_city: Başlangıç şehri
        """
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.start_city = start_city
        
        # Sonuçlar için
        self.best_route = None
        self.best_distance = float('inf')
        self.convergence_history = []
        
    def initialize_population(self):
        """Rastgele başlangıç popülasyonu oluştur"""
        population = []
        for _ in range(self.population_size):
            route = generate_random_route(self.n_cities, self.start_city)
            population.append(route)
        return population
    
    def fitness(self, route):
        """
        Fitness fonksiyonu (minimize edilecek)
        Daha kısa mesafe = daha iyi fitness
        """
        distance = calculate_route_distance(route, self.distance_matrix)
        # Sıfıra bölünmeyi önle
        return 1.0 / (distance + 1e-6)
    
    def selection(self, population, fitnesses):
        """
        Tournament Selection - En iyi bireyleri seç
        """
        tournament_size = 5
        selected = []
        
        for _ in range(len(population)):
            # Rastgele bireyler seç
            tournament_indices = np.random.choice(
                len(population), tournament_size, replace=False
            )
            tournament_fitnesses = [fitnesses[i] for i in tournament_indices]
            
            # En iyi fitness'a sahip olanı seç
            winner_index = tournament_indices[
                np.argmax(tournament_fitnesses)
            ]
            selected.append(population[winner_index].copy())
        
        return selected
    
    def order_crossover(self, parent1, parent2):
        """
        Order Crossover (OX) - TSP için uygun çaprazlama
        """
        if np.random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        size = len(parent1)
        
        # Rastgele iki nokta seç (1'den başla çünkü 0. indeks start_city)
        if size > 2:
            start, end = sorted(np.random.choice(range(1, size), 2, replace=False))
        else:
            return parent1.copy(), parent2.copy() # Yeterli şehir yoksa
        
        # Çocuk 1
        child1 = [-1] * size
        child1[0] = self.start_city  # Başlangıç şehri sabit
        child1[start:end] = parent1[start:end]
        
        # Parent2'den eksik şehirleri ekle
        pointer = end
        for city in parent2:
            if city not in child1:
                if pointer >= size:
                    pointer = 1  # Başlangıç şehrini atla
                child1[pointer] = city
                pointer += 1
        
        # Çocuk 2 (benzer şekilde)
        child2 = [-1] * size
        child2[0] = self.start_city
        child2[start:end] = parent2[start:end]
        
        pointer = end
        for city in parent1:
            if city not in child2:
                if pointer >= size:
                    pointer = 1
                child2[pointer] = city
                pointer += 1
        
        return child1, child2
    
    def swap_mutation(self, route):
        """
        Swap Mutation - İki şehrin yerini değiştir
        """
        if np.random.random() < self.mutation_rate:
            # Başlangıç şehri hariç iki şehir seç
            if len(route) > 2:
                idx1, idx2 = np.random.choice(range(1, len(route)), 2, replace=False)
                route[idx1], route[idx2] = route[idx2], route[idx1]
        
        return route
    
    def solve(self):
        """
        Genetik Algoritma ile TSP'yi çöz
        
        Returns:
            best_route: En iyi rota
            best_distance: En kısa mesafe
            execution_time: Çalışma süresi
        """
        start_time = time.time()
        
        # Başlangıç popülasyonu
        population = self.initialize_population()
        
        print(f"\n🧬 Genetik Algoritma Başlatıldı")
        print(f"   Popülasyon: {self.population_size}")
        print(f"   Nesil: {self.generations}")
        print(f"   Başlangıç Şehri: {self.start_city}")
        
        # İlk en iyiyi bul
        initial_distances = [calculate_route_distance(r, self.distance_matrix) for r in population]
        best_idx = np.argmin(initial_distances)
        self.best_route = population[best_idx].copy()
        self.best_distance = initial_distances[best_idx]
        self.convergence_history.append(self.best_distance)

        for generation in range(self.generations):
            # Fitness hesapla
            fitnesses = [self.fitness(route) for route in population]
            
            # En iyi bireyi bul
            # Fitness max olan, distance min olandır
            best_idx = np.argmax(fitnesses)
            best_route_gen = population[best_idx]
            best_distance_gen = calculate_route_distance(
                best_route_gen, self.distance_matrix
            )
            
            # Global en iyiyi güncelle
            if best_distance_gen < self.best_distance:
                self.best_distance = best_distance_gen
                self.best_route = best_route_gen.copy()
            
            # Yakınsama geçmişi
            self.convergence_history.append(self.best_distance)
            
            # İlerleme göster
            if generation % 50 == 0:
                print(f"   Nesil {generation}: En iyi mesafe = {self.best_distance:.2f}")
            
            # Seçilim
            selected = self.selection(population, fitnesses)
            
            # Yeni nesil oluştur
            new_population = []
            for i in range(0, len(selected), 2):
                parent1 = selected[i]
                parent2 = selected[i + 1] if i + 1 < len(selected) else selected[0]
                
                # Çaprazlama
                child1, child2 = self.order_crossover(parent1, parent2)
                
                # Mutasyon
                child1 = self.swap_mutation(child1)
                child2 = self.swap_mutation(child2)
                
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
        
        execution_time = time.time() - start_time
        
        print(f"\n✅ Genetik Algoritma Tamamlandı!")
        print(f"   En iyi mesafe: {self.best_distance:.2f}")
        print(f"   Çalışma süresi: {execution_time:.2f} saniye")
        
        return self.best_route, self.best_distance, execution_time
