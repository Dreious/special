import numpy as np
import pandas as pd
import os

def generate_data():
    # Dizinlerin mevcut olduğundan emin ol
    os.makedirs('data', exist_ok=True)
    
    # 1. Şehir Verisini Oluştur
    n_cities = 25
    cities_data = []
    
    for i in range(1, n_cities + 1):
        # 0 ile 100 arasında rastgele koordinatlar
        x = np.random.randint(0, 101)
        y = np.random.randint(0, 101)
        cities_data.append([i, x, y])
    
    df_cities = pd.DataFrame(cities_data, columns=['CityID', 'X_Coordinate', 'Y_Coordinate'])
    df_cities.to_csv('data/cityData.txt', index=False)
    print(f"Generated data/cityData.txt with {n_cities} cities.")
    
    # 2. Mesafe Matsini Oluştur
    distances_data = []
    
    coords = df_cities[['X_Coordinate', 'Y_Coordinate']].values
    
    for i in range(n_cities):
        for j in range(i + 1, n_cities):
            # Öklid mesafesi
            dist = np.sqrt(np.sum((coords[i] - coords[j])**2))
            
            # Şehir ID'leri gereksinimlere göre 1 tabanlıdır (City1, City2)
            # Satır formatı: City1, City2, Distance
            distances_data.append([i + 1, j + 1, dist])
            
    df_distances = pd.DataFrame(distances_data, columns=['City1', 'City2', 'Distance'])
    df_distances.to_csv('data/intercityDistance.txt', index=False)
    print(f"Generated data/intercityDistance.txt with {len(distances_data)} distances.")

if __name__ == "__main__":
    generate_data()
