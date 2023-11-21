from typing import List
import unittest


class BinarySet:
    def __init__(self, max_value: int, binary_set: List[bool] = None) -> None:
        self.max_value = max_value
        if binary_set is None:
            self.binary_set = [0] * (max_value + 1)
        else:
            self.binary_set = binary_set

    def from_number_set(self, number_set: List[int], max_value: int) -> None:
        if self.max_value < max_value:
            self.max_value = max_value
            self.binary_set = [0] * (self.max_value + 1)
        for num in number_set:
            self.binary_set[num] = 1

    def union(self, other_binary_set: "BinarySet") -> "BinarySet":
        result_set: List[bool] = [a or b for a, b in zip(self.binary_set, other_binary_set.binary_set)]
        return BinarySet(self.max_value, result_set)

    def intersection(self, other_binary_set: "BinarySet") -> "BinarySet":
        result_set: List[bool] = [a and b for a, b in zip(self.binary_set, other_binary_set.binary_set)]
        return BinarySet(self.max_value, result_set)

    def complement(self) -> "BinarySet":
        result_set: List[bool] = [1 - a for a in self.binary_set]
        return BinarySet(self.max_value, result_set)

    def difference(self, other_binary_set) -> "BinarySet":
        result_set: List[bool] = [a and not b for a, b in zip(self.binary_set, other_binary_set.binary_set)]
        return BinarySet(self.max_value, result_set)

    def __add__(self, other_binary_set: "BinarySet") -> "BinarySet":
        return self.union(other_binary_set)

    def __sub__(self, other_binary_set: "BinarySet") -> "BinarySet":
        return self.difference(other_binary_set)

    def __mul__(self, other_binary_set: "BinarySet") -> "BinarySet":
        return self.intersection(other_binary_set)

    def __invert__(self) -> "BinarySet":
        return self.complement()

    def __str__(self) -> str:
        return str(self.binary_set)

    def __repr__(self) -> str:
        return str(self.binary_set)


def int_to_binary(n: int) -> List[bool]:
    binary = []
    while n > 0:
        binary.append(n % 2)
        n = n // 2
    return binary


def generate_subsets(n: int) -> List[BinarySet]:
    subsets = []
    for i in range(2**n):
        subsets.append(BinarySet(n, int_to_binary(i)))
    return subsets


def generate_gray_code(n: int) -> List[str]:
    if n <= 0:
        return ['0']

    gray_code = ['0', '1']

    for i in range(1, n):
        reflected_gray_code = gray_code[::-1]
        gray_code = ['0' + code for code in gray_code] + ['1' + code for code in reflected_gray_code]

    return gray_code


class TestBinarySet(unittest.TestCase):
    def test_union(self):
        binary_set1 = BinarySet(3, [1, 0, 1])
        binary_set2 = BinarySet(3, [0, 1, 0])
        result = binary_set1 + binary_set2
        self.assertEqual(result.binary_set, [1, 1, 1])

    def test_intersection(self):
        binary_set1 = BinarySet(3, [1, 0, 1])
        binary_set2 = BinarySet(3, [0, 1, 1])
        result = binary_set1 * binary_set2
        self.assertEqual(result.binary_set, [0, 0, 1])

    def test_complement(self):
        binary_set1 = BinarySet(3, [1, 0, 1])
        result = ~ binary_set1
        self.assertEqual(result.binary_set, [0, 1, 0])
    
    def test_difference(self):
        binary_set1 = BinarySet(3, [1, 1, 1])
        binary_set2 = BinarySet(3, [0, 1, 0])
        result = binary_set1 - binary_set2
        self.assertEqual(result.binary_set, [1, 0, 1])


class TestGenerateSubsets(unittest.TestCase):
    def test_generate_subsets(self):
        subsets = generate_subsets(3)
        self.assertEqual(len(subsets), 8)


class TestGenerateGrayCode(unittest.TestCase):
    def test_generate_gray_code(self):
        print(generate_gray_code(2))
        print(generate_gray_code(3))
        gray_code_sequences = generate_gray_code(3)
        self.assertEqual(len(gray_code_sequences), 8)


if __name__ == '__main__':
    unittest.main()
    