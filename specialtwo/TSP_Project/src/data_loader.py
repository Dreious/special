import pandas as pd
import numpy as np
import os

class TSPDataLoader:
    """
    TSP veri dosyalarını yükleyen ve işleyen sınıf
    """
    
    def __init__(self, city_file='data/cityData.txt', 
                 distance_file='data/intercityDistance.txt'):
        """
        Args:
            city_file: Şehir koordinatları dosyası
            distance_file: Şehirler arası mesafe dosyası
        """
        # Yolları main.py'nin çalıştığı yere göre veya mutlak olarak ayarla
        # TSP_Project kök dizininden çalıştırıldığı varsayılıyor
        self.city_file = city_file
        self.distance_file = distance_file
        self.cities = None
        self.distance_matrix = None
        
    def load_cities(self):
        """Şehir koordinatlarını yükle"""
        if not os.path.exists(self.city_file):
            raise FileNotFoundError(f"Dosya bulunamadı: {self.city_file}")
            
        # cityData.txt formatı: ID X Y (boşlukla ayrılmış, başlık yok)
        cities_data = []
        with open(self.city_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    city_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    cities_data.append([city_id, x, y])
        
        self.cities = pd.DataFrame(cities_data, columns=['CityID', 'X_Coordinate', 'Y_Coordinate'])
        print(f"✓ {len(self.cities)} şehir yüklendi")
        return self.cities
    
    def load_distances(self):
        """Şehirler arası mesafeleri yükle ve matris oluştur"""
        if not os.path.exists(self.distance_file):
            raise FileNotFoundError(f"Dosya bulunamadı: {self.distance_file}")

        if self.cities is None:
            self.load_cities()
            
        n_cities = len(self.cities)
        
        # intercityDistance.txt formatı: tam mesafe matrisi (boşlukla ayrılmış)
        # Her satır bir şehrin diğer tüm şehirlere mesafelerini içerir
        distance_rows = []
        with open(self.distance_file, 'r') as f:
            for line in f:
                # Boşlukları temizle ve sayıları ayır
                parts = line.strip().split()
                if parts:
                    row = [float(val) for val in parts]
                    distance_rows.append(row)
        
        self.distance_matrix = np.array(distance_rows)
        
        # Matrisin boyutunu kontrol et
        if self.distance_matrix.shape[0] != n_cities or self.distance_matrix.shape[1] != n_cities:
            print(f"⚠ Uyarı: Mesafe matrisi boyutu ({self.distance_matrix.shape}) şehir sayısıyla ({n_cities}) eşleşmiyor")
            # Matris boyutunu şehir sayısına göre ayarla (eğer matris daha büyükse)
            if self.distance_matrix.shape[0] >= n_cities and self.distance_matrix.shape[1] >= n_cities:
                self.distance_matrix = self.distance_matrix[:n_cities, :n_cities]
        
        print(f"✓ Mesafe matrisi oluşturuldu ({self.distance_matrix.shape[0]}x{self.distance_matrix.shape[1]})")
        return self.distance_matrix
    
    def get_city_coordinates(self):
        """Şehir koordinatlarını numpy array olarak döndür"""
        if self.cities is None:
            return None
        return self.cities[['X_Coordinate', 'Y_Coordinate']].values
