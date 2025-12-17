import matplotlib.pyplot as plt
import numpy as np

class TSPVisualizer:
    """
    TSP sonuçlarını görselleştiren sınıf
    """
    
    def __init__(self, cities_df):
        """
        Args:
            cities_df: Şehir bilgilerini içeren DataFrame
        """
        self.cities = cities_df
    
    def plot_route(self, route, distance, algorithm_name, 
                   start_city, save_path=None):
        """
        Rotayı 2D grafikte göster
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Şehir koordinatları
        x_coords = self.cities['X_Coordinate'].values
        y_coords = self.cities['Y_Coordinate'].values
        
        # Tüm şehirleri çiz
        ax.scatter(x_coords, y_coords, c='lightblue', 
                  s=100, zorder=3, edgecolors='black', linewidth=1)
        
        # Şehir ID'lerini etiketle
        for idx, row in self.cities.iterrows():
            ax.annotate(str(row['CityID']), 
                       (row['X_Coordinate'], row['Y_Coordinate']),
                       fontsize=8, ha='center', va='center', fontweight='bold')
        
        # Rotayı çiz
        for i in range(len(route) - 1):
            city1 = route[i]
            city2 = route[i + 1]
            
            x1, y1 = x_coords[city1], y_coords[city1]
            x2, y2 = x_coords[city2], y_coords[city2]
            
            ax.plot([x1, x2], [y1, y2], 'r-', linewidth=1.5, alpha=0.7)
            
            # Ok işareti ekle (yön göstermek için)
            dx = x2 - x1
            dy = y2 - y1
            if abs(dx) > 0.1 or abs(dy) > 0.1: # Küçük oklar çizme
                ax.arrow(x1, y1, dx*0.8, dy*0.8, 
                        head_width=1.5, head_length=1.5, 
                        fc='red', ec='red', alpha=0.6)
        
        # Son şehirden başlangıca dön
        x1, y1 = x_coords[route[-1]], y_coords[route[-1]]
        x2, y2 = x_coords[route[0]], y_coords[route[0]]
        ax.plot([x1, x2], [y1, y2], 'r-', linewidth=1.5, alpha=0.7)
        
        # Başlangıç şehrini işaretle (Yeşil yıldız)
        ax.scatter(x_coords[start_city], y_coords[start_city], 
                  c='green', s=300, marker='*', 
                  zorder=5, edgecolors='darkgreen', linewidth=1.5,
                  label='Başlangıç/Bitiş')
        
        # Başlık ve etiketler
        ax.set_title(f'{algorithm_name} - TSP Çözümü\n'
                    f'Başlangıç Şehri: {start_city} | '
                    f'Toplam Mesafe: {distance:.2f} km',
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('X Koordinatı', fontsize=10)
        ax.set_ylabel('Y Koordinatı', fontsize=10)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Kaydet veya göster
        if save_path:
            plt.savefig(save_path, dpi=120, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_convergence(self, ga_history, pso_history, 
                        start_city, save_path=None):
        """
        İki algoritmanın yakınsama grafiğini çiz
        """
        fig, ax = plt.subplots(figsize=(8, 5))
        
        ax.plot(ga_history, label='Genetik Algoritma', 
               linewidth=2, color='blue')
        ax.plot(pso_history, label='Parçacık Sürü Optimizasyonu', 
               linewidth=2, color='red')
        
        ax.set_title(f'Algoritma Yakınsama Karşılaştırması\n'
                    f'Başlangıç Şehri: {start_city}',
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('İterasyon/Nesil', fontsize=10)
        ax.set_ylabel('En İyi Mesafe (km)', fontsize=10)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=120, bbox_inches='tight')
            print(f"✓ Yakınsama grafiği kaydedildi: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_comparison_bar(self, results_dict, save_path=None):
        """
        Farklı başlangıç şehirleri için sonuçları bar grafikte göster
        """
        start_cities = list(results_dict.keys())
        ga_distances = [results_dict[sc]['GA'] for sc in start_cities]
        pso_distances = [results_dict[sc]['PSO'] for sc in start_cities]
        
        x = np.arange(len(start_cities))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        bars1 = ax.bar(x - width/2, ga_distances, width, 
                      label='Genetik Algoritma', color='blue', alpha=0.7)
        bars2 = ax.bar(x + width/2, pso_distances, width, 
                      label='PSO', color='red', alpha=0.7)
        
        ax.set_title('Farklı Başlangıç Şehirleri için Algoritma Karşılaştırması',
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('Başlangıç Şehri', fontsize=10)
        ax.set_ylabel('Toplam Mesafe (km)', fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels([str(c) for c in start_cities], fontsize=9)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Bar değerlerini göster
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=120, bbox_inches='tight')
            print(f"✓ Karşılaştırma grafiği kaydedildi: {save_path}")
        else:
            plt.show()
        
        plt.close()
