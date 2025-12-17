import numpy as np
from utils import calculate_route_distance, generate_random_route
import time

class ParticleSwarmTSP:
    """
    Parçacık Sürü Optimizasyonu (PSO) ile TSP çözümü
    """
    
    def __init__(self, distance_matrix, n_particles=50, 
                 iterations=500, w=0.5, c1=1.5, c2=1.5, start_city=0):
        """
        Args:
            distance_matrix: Şehirler arası mesafe matrisi
            n_particles: Parçacık sayısı
            iterations: Maksimum iterasyon
            w: İnertia ağırlığı
            c1: Bilişsel parametre
            c2: Sosyal parametre
            start_city: Başlangıç şehri
        """
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.n_particles = n_particles
        self.iterations = iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.start_city = start_city
        
        self.best_route = None
        self.best_distance = float('inf')
        self.convergence_history = []
    
    def initialize_particles(self):
        """Parçacıkları başlat"""
        particles = []
        velocities = []
        personal_best = []
        personal_best_distances = []
        
        for _ in range(self.n_particles):
            # Rastgele rota oluştur
            route = generate_random_route(self.n_cities, self.start_city)
            particles.append(route)
            
            # Velocity (hız) - başlangıçta rastgele swap operasyonları
            velocities.append([])
            
            # Personal best
            personal_best.append(route.copy())
            distance = calculate_route_distance(route, self.distance_matrix)
            personal_best_distances.append(distance)
        
        return particles, velocities, personal_best, personal_best_distances
    
    def apply_swap_sequence(self, route, swap_sequence):
        """Swap operasyonlarını uygula"""
        new_route = route.copy()
        for i, j in swap_sequence:
            if i != 0 and j != 0:  # Başlangıç şehrini değiştirme
                new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route
    
    def generate_swap_sequence(self, route1, route2):
        """İki rota arasındaki farkı swap dizisi olarak oluştur"""
        swap_sequence = []
        # route2'yi referans alarak route1'i ona benzetmeye çalışacağız
        # Ancak bunu yaparken route1 kopyası üzerinde işlem yaparak diziyi bulmalıyız
        temp_route = route1.copy()
        
        for i in range(1, len(route1)):  # Başlangıç şehrini atla
            target_city = route2[i]
            if temp_route[i] != target_city:
                # target_city'nin temp_route'daki pozisyonunu bul
                if target_city in temp_route:
                    j = temp_route.index(target_city)
                    swap_sequence.append((i, j))
                    # Swap yap
                    temp_route[i], temp_route[j] = temp_route[j], temp_route[i]
        
        return swap_sequence
    
    def solve(self):
        """
        PSO ile TSP'yi çöz
        """
        start_time = time.time()
        
        # Parçacıkları başlat
        particles, velocities, personal_best, personal_best_distances = \
            self.initialize_particles()
        
        # Global best
        global_best_idx = np.argmin(personal_best_distances)
        global_best = personal_best[global_best_idx].copy()
        global_best_distance = personal_best_distances[global_best_idx]
        
        print(f"\n🌊 Parçacık Sürü Optimizasyonu Başlatıldı")
        print(f"   Parçacık sayısı: {self.n_particles}")
        print(f"   İterasyon: {self.iterations}")
        print(f"   Başlangıç Şehri: {self.start_city}")
        
        # İlk iterasyonu kaydet
        self.convergence_history.append(global_best_distance)
        
        for iteration in range(self.iterations):
            for i in range(self.n_particles):
                # Velocity güncelle (swap dizileri)
                # Pbest'e giden yol
                cognitive_component = self.generate_swap_sequence(
                    particles[i], personal_best[i]
                )
                # Gbest'e giden yol
                social_component = self.generate_swap_sequence(
                    particles[i], global_best
                )
                
                # Rastgele seçim yap
                # Basitçe componentlerden rastgele bir alt küme seçiyoruz
                
                new_velocity = []
                
                # Cognitive (Bilişsel) katkı
                if cognitive_component:
                    n_cognitive = int(self.c1 * len(cognitive_component) * np.random.random())
                    # Mevcut olandan daha fazla örneklememeyi sağla
                    n_cognitive = min(n_cognitive, len(cognitive_component))
                    if n_cognitive > 0:
                        selected_indices = np.random.choice(len(cognitive_component), size=n_cognitive, replace=False)
                        for idx in selected_indices:
                            new_velocity.append(cognitive_component[idx])
                
                # Social (Sosyal) katkı
                if social_component:
                    n_social = int(self.c2 * len(social_component) * np.random.random())
                    # Mevcut olandan daha fazla örneklememeyi sağla
                    n_social = min(n_social, len(social_component))
                    if n_social > 0:
                        selected_indices = np.random.choice(len(social_component), size=n_social, replace=False)
                        for idx in selected_indices:
                            new_velocity.append(social_component[idx])
                
                # Pozisyon güncelle
                particles[i] = self.apply_swap_sequence(particles[i], new_velocity)
                
                # Fitness hesapla
                distance = calculate_route_distance(particles[i], self.distance_matrix)
                
                # Personal best güncelle
                if distance < personal_best_distances[i]:
                    personal_best[i] = particles[i].copy()
                    personal_best_distances[i] = distance
                    
                    # Global best güncelle
                    if distance < global_best_distance:
                        global_best = particles[i].copy()
                        global_best_distance = distance
            
            # Yakınsama geçmişi
            self.convergence_history.append(global_best_distance)
            
            # İlerleme göster
            if iteration % 50 == 0:
                print(f"   İterasyon {iteration}: En iyi mesafe = {global_best_distance:.2f}")
        
        self.best_route = global_best
        self.best_distance = global_best_distance
        
        execution_time = time.time() - start_time
        
        print(f"\n✅ PSO Tamamlandı!")
        print(f"   En iyi mesafe: {self.best_distance:.2f}")
        print(f"   Çalışma süresi: {execution_time:.2f} saniye")
        
        return self.best_route, self.best_distance, execution_time
