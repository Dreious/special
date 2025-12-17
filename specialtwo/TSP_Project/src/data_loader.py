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
            
        # cityData.txt formatı: CityID, X_Coordinate, Y_Coordinate
        self.cities = pd.read_csv(self.city_file)
        print(f"✓ {len(self.cities)} şehir yüklendi")
        return self.cities
    
    def load_distances(self):
        """Şehirler arası mesafeleri yükle ve matris oluştur"""
        if not os.path.exists(self.distance_file):
            raise FileNotFoundError(f"Dosya bulunamadı: {self.distance_file}")

        # intercityDistance.txt formatı: City1, City2, Distance
        distances = pd.read_csv(self.distance_file)
        
        if self.cities is None:
            self.load_cities()
            
        # Mesafe matrisini oluştur
        n_cities = len(self.cities)
        self.distance_matrix = np.zeros((n_cities, n_cities))
        
        for _, row in distances.iterrows():
            city1 = int(row['City1']) - 1  # 0-indexed
            city2 = int(row['City2']) - 1
            distance = float(row['Distance'])
            
            self.distance_matrix[city1][city2] = distance
            self.distance_matrix[city2][city1] = distance  # Simetrik matris
        
        print(f"✓ Mesafe matrisi oluşturuldu ({n_cities}x{n_cities})")
        return self.distance_matrix
    
    def get_city_coordinates(self):
        """Şehir koordinatlarını numpy array olarak döndür"""
        if self.cities is None:
            return None
        return self.cities[['X_Coordinate', 'Y_Coordinate']].values
