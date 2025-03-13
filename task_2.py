import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

class SplayTree:
    class Node:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value
            self.left = self.right = None

    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)

        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            return root if root.right is None else self._left_rotate(root)

    def _left_rotate(self, root):
        right_node = root.right
        root.right = right_node.left
        right_node.left = root
        return right_node

    def _right_rotate(self, root):
        left_node = root.left
        root.left = left_node.right
        left_node.right = root
        return left_node

    def insert(self, key, value):
        if self.root is None:
            self.root = self.Node(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
            return
        new_node = self.Node(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        if self.root is None:
            return None
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

def fibonacci_splay(n, tree):
    value = tree.search(n)
    if value is not None:
        return value
    if n <= 1:
        tree.insert(n, n)
        return n
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

n_values = list(range(0, 951, 50))  
lru_times = []
splay_times = []

for n in n_values:
    start_time = timeit.default_timer()
    fibonacci_lru(n)
    end_time = timeit.default_timer()
    lru_times.append(end_time - start_time)

    start_time = timeit.default_timer()
    tree = SplayTree()
    fibonacci_splay(n, tree)
    end_time = timeit.default_timer()
    splay_times.append(end_time - start_time)

plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label='LRU Cache Time', marker='o')
plt.plot(n_values, splay_times, label='Splay Tree Time', marker='x')
plt.xlabel('n (Fibonacci number)')
plt.ylabel('Time (seconds)')
plt.title('Performance Comparison: LRU Cache vs Splay Tree')
plt.legend()
plt.grid(True)
plt.show()

print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)'}")
print('-' * 50)
for n, lru, splay in zip(n_values, lru_times, splay_times):
    print(f"{n:<10}{lru:<25}{splay}")

