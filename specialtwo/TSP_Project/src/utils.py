import numpy as np

def calculate_route_distance(route, distance_matrix):
    """
    Verilen rota için toplam mesafeyi hesapla
    
    Args:
        route: Şehir ID'lerinin sırası [0, 3, 1, 4, 2, 0]
        distance_matrix: Şehirler arası mesafe matrisi
    
    Returns:
        total_distance: Toplam rota mesafesi
    """
    total_distance = 0
    
    for i in range(len(route) - 1):
        city_from = route[i]
        city_to = route[i + 1]
        total_distance += distance_matrix[city_from][city_to]
    
    # Son şehirden başlangıca dön
    total_distance += distance_matrix[route[-1]][route[0]]
    
    return total_distance


def generate_random_route(n_cities, start_city=0):
    """
    Rastgele bir rota oluştur
    
    Args:
        n_cities: Toplam şehir sayısı
        start_city: Başlangıç şehri ID'si
    
    Returns:
        route: Rastgele rota dizisi
    """
    # Başlangıç şehri hariç diğer şehirleri karıştır
    other_cities = [i for i in range(n_cities) if i != start_city]
    np.random.shuffle(other_cities)
    
    # Başlangıç şehrini başa ekle
    route = [start_city] + other_cities
    
    return route


def is_valid_route(route, n_cities):
    """
    Rotanın geçerli olup olmadığını kontrol et
    
    Args:
        route: Kontrol edilecek rota
        n_cities: Toplam şehir sayısı
    
    Returns:
        bool: Geçerli ise True
    """
    # Her şehir tam olarak bir kez geçmeli
    return len(route) == n_cities and len(set(route)) == n_cities
