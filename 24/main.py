from typing import List, Tuple, Optional
from itertools import combinations


def parse_hailstones(lines: List[str]) -> List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:
    # Parse lines like "19, 13, 30 @ -2,  1, -2" into ((px, py, pz), (vx, vy, vz))
    hailstones = []
    
    for line in lines:
        pos, vel = line.split('@')
        px, py, pz = map(int, pos.split(','))
        vx, vy, vz = map(int, vel.split(','))
        hailstones.append(((px, py, pz), (vx, vy, vz)))
    
    return hailstones


def matrix_det(m: List[List[float]]) -> float:
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    
    determinant = 0
    for c in range(len(m)):
        minor = [row[:c] + row[c + 1:] for row in m[1:]]
        determinant += ((-1) ** c) * m[0][c] * matrix_det(minor)
    
    return determinant


def intersection_2d(hailstone_a: Tuple, hailstone_b: Tuple) -> Optional[Tuple[float, float]]:
    (ax, ay, _), (vax, vay, _) = hailstone_a
    (bx, by, _), (vbx, vby, _) = hailstone_b
    
    # Calculate intersection point using line intersection formula
    a1 = (ax + vax, ay + vay)
    b1 = (bx + vbx, by + vby)
    
    dx = (ax - a1[0], bx - b1[0])
    dy = (ay - a1[1], by - b1[1])
    
    div = matrix_det([list(dx), list(dy)])
    if div == 0:
        return None
    
    d = (matrix_det([[ax, ay], [a1[0], a1[1]]]), matrix_det([[bx, by], [b1[0], b1[1]]]))
    
    x = matrix_det([list(d), list(dx)]) / div
    y = matrix_det([list(d), list(dy)]) / div
    
    # Check if intersection is in the future for both hailstones
    if (x > ax) != (vax > 0) or (x > bx) != (vbx > 0):
        return None
    
    if (y > ay) != (vay > 0) or (y > by) != (vby > 0):
        return None
    
    return x, y


def solve_part_1(lines: List[str]) -> int:
    hailstones = parse_hailstones(lines)
    
    # Define test area bounds
    min_bound = 200000000000000
    max_bound = 400000000000000
    
    count = 0
    
    for a, b in combinations(hailstones, 2):
        result = intersection_2d(a, b)
        
        if result is None:
            continue
        
        x, y = result
        
        if min_bound <= x <= max_bound and min_bound <= y <= max_bound:
            count += 1
    
    return count


def matrix_transpose(m: List[List[float]]) -> List[List[float]]:
    return list(map(list, zip(*m)))


def matrix_minor(m: List[List[float]], i: int, j: int) -> List[List[float]]:
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def matrix_inverse(m: List[List[float]]) -> List[List[float]]:
    # Calculate matrix inverse using cofactors
    determinant = matrix_det(m)
    cofactors = []
    
    for r in range(len(m)):
        row = []
        for c in range(len(m)):
            minor = matrix_minor(m, r, c)
            row.append(((-1) ** (r + c)) * matrix_det(minor))
        cofactors.append(row)
    
    cofactors = matrix_transpose(cofactors)
    
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] /= determinant
    
    return cofactors


def get_cross_product_equations(a: Tuple, va: Tuple, b: Tuple, vb: Tuple) -> Tuple:
    # Build equations from cross product identity: (p - a) X (v - va) == (p - b) X (v - vb)
    dx, dy, dz = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    dvx, dvy, dvz = va[0] - vb[0], va[1] - vb[1], va[2] - vb[2]
    
    # Coefficient matrix A and constant terms B for 3 equations
    A = [
        [0, -dvz, dvy, 0, -dz, dy],
        [dvz, 0, -dvx, dz, 0, -dx],
        [-dvy, dvx, 0, -dy, dx, 0]
    ]
    
    B = [
        b[1] * vb[2] - b[2] * vb[1] - (a[1] * va[2] - a[2] * va[1]),
        b[2] * vb[0] - b[0] * vb[2] - (a[2] * va[0] - a[0] * va[2]),
        b[0] * vb[1] - b[1] * vb[0] - (a[0] * va[1] - a[1] * va[0])
    ]
    
    return A, B


def matrix_mul(m: List[List[float]], vec: List[float]) -> List[float]:
    result = []
    for row in m:
        result.append(sum(r * v for r, v in zip(row, vec)))
    return result


def solve_part_2(lines: List[str]) -> int:
    hailstones = parse_hailstones(lines)
    
    # Take first 3 hailstones to solve for rock position (x, y, z) and velocity (vx, vy, vz)
    (a, va), (b, vb), (c, vc) = hailstones[:3]
    
    # Build system of 6 equations from cross product identities
    A1, B1 = get_cross_product_equations(a, va, b, vb)
    A2, B2 = get_cross_product_equations(a, va, c, vc)
    
    A = A1 + A2
    B = B1 + B2
    
    # Solve linear system: A * [x, y, z, vx, vy, vz]^T = B
    solution = matrix_mul(matrix_inverse(A), B)
    
    # Return sum of rock position coordinates (x + y + z)
    return sum(map(round, solution[:3]))


if __name__ == "__main__":
    with open("24/input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(f"Part 1: {solve_part_1(lines)}")
    print(f"Part 2: {solve_part_2(lines)}")