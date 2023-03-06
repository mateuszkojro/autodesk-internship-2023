"""
Write a program in Python which:
- accepts as an input a number of points,
- generates that many points on a 2d plane in the range [-100; 100] for both axes,
- finds and prints three points from which the smallest triangle can be built.

What kind of error handling would you implement? How to validate that the triangle is valid? How to speed up the algorithm to avoid calculating all possible combinations?
"""
import argparse
from typing import Any, Tuple
import numpy as np
import heapq

def calculate_triangle_perimeter(points: np.ndarray) -> float:
    return float(
        np.linalg.norm(points[1] - points[0])
        + np.linalg.norm(points[2] - points[1])
        + np.linalg.norm(points[2] - points[0])
    )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("points", type=int, help="Number of points")
    parser.add_argument("--plot", action="store_true", help="Plot points")
    return parser.parse_args()


def generate_points(number_of_points: int) -> np.ndarray:
    return np.random.randint(-100, 100, size=(number_of_points, 2))


def is_triangle_valid(points: np.ndarray) -> bool:
    assert len(points) == 3
    ab = points[1] - points[0]
    bc = points[2] - points[1]
    ac = points[2] - points[0]
    if np.dot(ab, bc) == 0 or np.dot(ab, ac) == 0 or np.dot(bc, ac) == 0:
        return False
    return True


def find_smallest_triangle_naive(points: np.ndarray, size_func) -> np.ndarray:
    min_area = np.inf
    min_points = np.array([])
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                if not is_triangle_valid(points[[i, j, k]]):
                    continue
                area = size_func(points[[i, j, k]])
                if area > 0 and area < min_area:
                    min_area = area
                    min_points = points[[i, j, k]]
    return min_points

def find_smallest_triangle(points: np.ndarray, size_func) -> np.ndarray:
    return find_smallest_triangle_naive(points, size_func)

def smallest_triangle_improved(points):
    points_distance = {}
    for i in range(len(points)):
        heap = []
        for j in range(len(points)):
            if i == j:
                continue
            heapq.heappush(heap, (np.linalg.norm(points[i] - points[j]), j))
        points_distance[i] = heap
        
    min_perimeter = np.inf
    min_triangle = np.array([])
    for i in range(len(points)):
        points_distance_copy = points_distance.copy()
        distance, closest_to_i = heapq.heappop(points_distance_copy[i])
        distance_third_point, third_point = heapq.heappop(points_distance_copy[closest_to_i])
        while third_point == i:
            distance_third_point, third_point = heapq.heappop(points_distance_copy[closest_to_i])
            
        if not is_triangle_valid(points[[i, closest_to_i, third_point]]):
            continue
        
        perimeter = calculate_triangle_perimeter(points[[i, closest_to_i, third_point]])
        if perimeter < min_perimeter:
            min_perimeter = perimeter
            min_triangle = points[[i, closest_to_i, third_point]]
            
    return min_triangle
        
def main():
    args = parse_args()
    points = generate_points(args.points)
    smallest_triangle_fast = smallest_triangle_improved(points)
    smallest_triangle = find_smallest_triangle_naive(points, calculate_triangle_perimeter)
    print("Smallest triangle (naive):", smallest_triangle)
    print("Smallest triangle (fast):", smallest_triangle_fast)
    if args.plot:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Please install matplotlib to plot points")
            return
        plt.scatter(points[:, 0], points[:, 1])
        plt.scatter(smallest_triangle[:, 0], smallest_triangle[:, 1], c="red")
        plt.scatter(smallest_triangle_fast[:, 0], smallest_triangle_fast[:, 1], c="green")
        plt.show()


if __name__ == "__main__":
    main()
