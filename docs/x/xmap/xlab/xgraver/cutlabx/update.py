from sklearn.cluster import DBSCAN

# Получаем координаты всех белых пикселей
points = np.column_stack(np.where(thresh > 0))

# Кластеризуем точки, которые находятся ближе 10 пикселей друг к другу
db = DBSCAN(eps=10, min_samples=5).fit(points)

# Теперь db.labels_ содержит номер кластера для каждой точки
