To install and run just download the dist folder and run the binary.

# Crafting Search Optimization

This project solves a combinatorics problem in a crafting system.

## The Setup

- A crafted item requires 6 ingredients
- The order of ingredients matters
- There are hundreds of possible ingredients
- Different orders produce different results

If you attempt to evaluate every possible ordered configuration from a large ingredient pool, the problem trends toward:

O(n^n)

---

## The Approach

Instead of evaluating every ordered permutation directly, I restructured the search.

### 1. Unordered Rough Scoring

Before considering order, I compute an unordered approximation score for ingredient sets.

This acts as a coarse filter that eliminates weak combinations early.

This reduces the effective search from something resembling O(n^n) toward a factorial search space:

O(n!)

While still large, this is dramatically more manageable in practice.

---

### 2. Weighted Priority Queue

Promising candidates are inserted into a priority queue.

Priority is computed as:

priority = distance * similarity_weight

