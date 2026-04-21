import numpy as np
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'cities.csv')
data = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')
points = data.values

def kmeans_gradient_descent(points, k, max_iter=100, lr=0.01):
    np.random.seed(42)
    centroids = points[np.random.choice(len(points), k, replace=False)].copy()
    
    for _ in range(max_iter):
        distances = np.sqrt(((points[:, np.newaxis] - centroids) ** 2).sum(axis=2))
        labels = np.argmin(distances, axis=1)
        
        grad = np.zeros_like(centroids)
        for i in range(k):
            mask = labels == i
            if mask.sum() > 0:
                grad[i] = -2 * (points[mask] - centroids[i]).sum(axis=0)
        
        centroids -= lr * grad
    
    distances = np.sqrt(((points[:, np.newaxis] - centroids) ** 2).sum(axis=2))
    labels = np.argmin(distances, axis=1)
    
    total_cost = 0
    for i in range(k):
        mask = labels == i
        if mask.sum() > 0:
            total_cost += ((points[mask] - centroids[i]) ** 2).sum()
    
    return centroids, labels, total_cost

def kmeans_newton_raphson(points, k, max_iter=20):
    np.random.seed(42)
    centroids = points[np.random.choice(len(points), k, replace=False)].copy()
    
    for _ in range(max_iter):
        distances = np.sqrt(((points[:, np.newaxis] - centroids) ** 2).sum(axis=2))
        labels = np.argmin(distances, axis=1)
        
        for i in range(k):
            mask = labels == i
            if mask.sum() > 0:
                cluster_points = points[mask]
                n = len(cluster_points)
                gradient = -2 * (cluster_points - centroids[i]).sum(axis=0)
                hessian = 2 * n * np.eye(2)
                
                try:
                    delta = np.linalg.solve(hessian, gradient)
                    centroids[i] -= delta
                except:
                    pass
    
    distances = np.sqrt(((points[:, np.newaxis] - centroids) ** 2).sum(axis=2))
    labels = np.argmin(distances, axis=1)
    
    total_cost = 0
    for i in range(k):
        mask = labels == i
        if mask.sum() > 0:
            total_cost += ((points[mask] - centroids[i]) ** 2).sum()
    
    return centroids, labels, total_cost

k = 3

centroids_gd, labels_gd, cost_gd = kmeans_gradient_descent(points, k)
centroids_nr, labels_nr, cost_nr = kmeans_newton_raphson(points, k)

print("Gradient Descent Method:")
print("Centroids:")
for i, c in enumerate(centroids_gd):
    print(f"  Airport {i+1}: ({c[0]:.3f}, {c[1]:.3f})")
print(f"Sum of squared distances: {cost_gd:.3f}")
print()

print("Newton-Raphson Method:")
print("Centroids:")
for i, c in enumerate(centroids_nr):
    print(f"  Airport {i+1}: ({c[0]:.3f}, {c[1]:.3f})")
print(f"Sum of squared distances: {cost_nr:.3f}")
print()

print("Comparison:")
print(f"Gradient Descent cost: {cost_gd:.3f}")
print(f"Newton-Raphson cost: {cost_nr:.3f}")
if cost_gd < cost_nr:
    print("Gradient Descent is better")
elif cost_nr < cost_gd:
    print("Newton-Raphson is better")
else:
    print("Both are equal")