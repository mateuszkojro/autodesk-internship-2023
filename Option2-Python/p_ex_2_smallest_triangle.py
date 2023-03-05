"""
Write a program in Python which:
- accepts as an input a number of points,
- generates that many points on a 2d plane in the range [-100; 100] for both axes,
- finds and prints three points from which the smallest triangle can be built.

What kind of error handling would you implement? How to validate that the triangle is valid? How to speed up the algorithm to avoid calculating all possible combinations?
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt

def calculate_triangle_area(points: np.ndarray) -> float:
    return 0.5 * float(np.linalg.norm(np.cross(points[1] - points[0], points[2] - points[0])))

def calculate_triangle_area_heron(points: np.ndarray) -> float:
    a = np.linalg.norm(points[1] - points[0])
    b = np.linalg.norm(points[2] - points[1])
    c = np.linalg.norm(points[2] - points[0])
    s = (a + b + c) / 2
    return np.sqrt(s * (s - a) * (s - b) * (s - c))

def calculate_triangle_perimeter(points: np.ndarray) -> float:
    return float(np.linalg.norm(points[1] - points[0]) + np.linalg.norm(points[2] - points[1]) + np.linalg.norm(points[2] - points[0]))

TRIANGLE_SIZE_FUNCTIONS = {
    "area": calculate_triangle_area,
    "area_heron": calculate_triangle_area_heron,
    "perimeter": calculate_triangle_perimeter,
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("points", type=int, help="Number of points")
    parser.add_argument("--plot", action="store_true", help="Plot points")
    parser.add_argument("--size-func", default="area", choices=TRIANGLE_SIZE_FUNCTIONS.keys(), help="Size function")
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

def main():
    args = parse_args()
    points = generate_points(args.points)
    size_func = TRIANGLE_SIZE_FUNCTIONS[args.size_func]
    smallest_triangle = find_smallest_triangle(points, size_func)
    print(smallest_triangle, calculate_triangle_perimeter(smallest_triangle))
    if args.plot:
        plt.scatter(points[:, 0], points[:, 1])
        plt.scatter(smallest_triangle[:, 0], smallest_triangle[:, 1], c="red")
        plt.show()


if __name__ == "__main__":
    main()