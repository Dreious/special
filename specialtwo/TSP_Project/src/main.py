from data_loader import TSPDataLoader
from genetic_algorithm import GeneticAlgorithmTSP
from particle_swarm import ParticleSwarmTSP
from visualizer import TSPVisualizer
import os
import sys

# Eğer üst dizinden çalıştırılıyorsa src'yi yola ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """
    TSP Projesi Ana Program
    """
    print("="*60)
    print("🚀 TSP PROJESİ - EVRİMSEL ALGORİTMALAR")
    print("="*60)
    
    # Yollar (çalıştırma bağlamı için ayarlanıyor)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')
    
    city_file = os.path.join(data_dir, 'cityData.txt')
    distance_file = os.path.join(data_dir, 'intercityDistance.txt')

    # 1. VERİ YÜKLEME
    print("\n📂 Veri yükleniyor...")
    loader = TSPDataLoader(
        city_file=city_file,
        distance_file=distance_file
    )
    cities = loader.load_cities()
    distance_matrix = loader.load_distances()
    
    # Görselleştirici
    visualizer = TSPVisualizer(cities)
    
    # 2. 5 FARKLI BAŞLANGIÇ ŞEHRİ
    start_cities = [0, 5, 10, 15, 20]  # Örnek şehirler - verimiz 25 şehir olduğu için bunlar geçerli
    
    results = {}
    
    # Sonuç klasörü oluştur
    os.makedirs(results_dir, exist_ok=True)
    
    # 3. HER BAŞLANGIÇ ŞEHRİ İÇİN ÇALIŞTIR
    for start_city in start_cities:
        print(f"\n{'='*60}")
        print(f"📍 SENARYO: Başlangıç Şehri = {start_city}")
        print(f"{'='*60}")
        
        results[start_city] = {}
        
        # A. GENETİK ALGORİTMA
        print("\n--- Genetik Algoritma ---")
        ga = GeneticAlgorithmTSP(
            distance_matrix=distance_matrix,
            population_size=100,
            generations=200, # Daha hızlı test tekrarı için azaltıldı, artırılabilir
            mutation_rate=0.02,
            crossover_rate=0.9,
            start_city=start_city
        )
        ga_route, ga_distance, ga_time = ga.solve()
        results[start_city]['GA'] = ga_distance
        
        # Görselleştir
        visualizer.plot_route(
            route=ga_route,
            distance=ga_distance,
            algorithm_name='Genetik Algoritma',
            start_city=start_city,
            save_path=os.path.join(results_dir, f'GA_city{start_city}.png')
        )
        
        # B. PARÇACIK SÜRÜ OPTİMİZASYONU
        print("\n--- Parçacık Sürü Optimizasyonu ---")
        pso = ParticleSwarmTSP(
            distance_matrix=distance_matrix,
            n_particles=50,
            iterations=200, # Adil karşılaştırma için GA ile aynı
            w=0.5,
            c1=1.5,
            c2=1.5,
            start_city=start_city
        )
        pso_route, pso_distance, pso_time = pso.solve()
        results[start_city]['PSO'] = pso_distance
        
        # Görselleştir
        visualizer.plot_route(
            route=pso_route,
            distance=pso_distance,
            algorithm_name='Parçacık Sürü Optimizasyonu',
            start_city=start_city,
            save_path=os.path.join(results_dir, f'PSO_city{start_city}.png')
        )
        
        # C. YAKINSAMA GRAFİĞİ
        visualizer.plot_convergence(
            ga_history=ga.convergence_history,
            pso_history=pso.convergence_history,
            start_city=start_city,
            save_path=os.path.join(results_dir, f'convergence_city{start_city}.png')
        )
        
        # D. SONUÇLARI YAZDIR
        print(f"\n📊 SONUÇLAR (Başlangıç Şehri: {start_city}):")
        print(f"   GA  - Mesafe: {ga_distance:.2f} km | Süre: {ga_time:.2f}s")
        print(f"   PSO - Mesafe: {pso_distance:.2f} km | Süre: {pso_time:.2f}s")
        
        better = "GA" if ga_distance < pso_distance else "PSO"
        print(f"   🏆 Kazanan: {better}")
    
    # 4. GENEL KARŞILAŞTIRMA
    print(f"\n{'='*60}")
    print("📈 GENEL KARŞILAŞTIRMA")
    print(f"{'='*60}")
    
    visualizer.plot_comparison_bar(
        results_dict=results,
        save_path=os.path.join(results_dir, 'overall_comparison.png')
    )
    
    # Özet tablo
    print("\n📋 ÖZET TABLO:")
    print(f"{'Başlangıç':<12} {'GA Mesafe':<15} {'PSO Mesafe':<15} {'Kazanan':<10}")
    print("-" * 60)
    for city in start_cities:
        ga_dist = results[city]['GA']
        pso_dist = results[city]['PSO']
        winner = "GA" if ga_dist < pso_dist else "PSO"
        print(f"{city:<12} {ga_dist:<15.2f} {pso_dist:<15.2f} {winner:<10}")
    
    print(f"\n{'='*60}")
    print("✅ PROJE TAMAMLANDI!")
    print(f"   Sonuçlar '{results_dir}' klasöründe kaydedildi")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
