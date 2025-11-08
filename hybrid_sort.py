import math
import random
import time
import gc
import sys

# Part 1: Algorithms Implementations From Book

def insertion_sort(A, p, r):
    """
    Sorts the subarray A[p..r] (inclusive) in-place.
    Based on page 14 of the book
    """
    # In our 0-based translation for a subarray A[p..r],
    # we start from the second element of the subarray (at index p+1).
    for j in range(p + 1, r + 1):
        key = A[j]
        # Insert A[j] into the sorted sequence A[p..j-1]
        i = j - 1
        while i >= p and A[i] > key:
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = key

def merge(A, p, q, r):
    """
    Merges the two sorted subarrays A[p..q] and A[q+1..r].
    From page 25 in the book 
    Note we use 0 indexed arrays.
    """
    n1 = q - p + 1
    n2 = r - q 

    # Hack to created lists in vanilla python
    L = [None] * (n1+1)
    R = [None] * (n2+1)

    for i in range(n1):
        L[i] = A[p + i]
    for j in range(n2):
        R[j] = A[q + 1 + j]

    L[n1] = math.inf
    R[n2] = math.inf

    i = 0
    j = 0

    for k in range(p, r + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i = i + 1
        else:
            A[k] = R[j]
            j = j + 1

def hybrid_merge_sort(A, p, r, k):
    """
    Sorts the subarray A[p..r] (inclusive) using the hybrid algorithm     
    It uses Insertion Sort for subarrays of size 'k' or less.
    """
    n = r - p + 1
    
    if n <= k:
        # Switch to insertion_sort for this small subarray
        insertion_sort(A, p, r)
    elif p < r:
        # If the subarray is larger than k, divide and conquer as usual.
        q = (p + r) // 2
        hybrid_merge_sort(A, p, q, k)
        hybrid_merge_sort(A, q + 1, r, k)
        merge(A, p, q, r)



# Part 2: Empirical Benchmark to Find Optimal K

def generate_random_array(n):
    """
    Generates an array of size n containing a
    uniform random permutation of the integers [0, n-1].
    """
    arr = list(range(n))
    random.shuffle(arr)
    return arr

def is_sorted(A):
    """Helper function to check if an array is sorted."""
    return A == sorted(A)

def find_optimal_k(N_SIZE=5000, K_MAX=50):
    """
    Runs an empirical test to find the optimal 'k' value.

    It times the execution of hybrid_merge_sort on a large, random
    array for various values of k and identifies which 'k'
    results in the minimum execution time.
    
    Returns:
        int: The optimal 'k' value found.
    """
    NUM_RUNS = 3
    
    # Set a high recursion depth to handle large arrays
    try:
        sys.setrecursionlimit(N_SIZE + 10)
    except Exception as e:
        print(f"Warning: Could not set recursion depth. {e}", file=sys.stderr)

    # --- Data Generation ---
    # Generate one master array. We will *copy* this for each test.
    # This is crucial to avoid a benchmark bias where sorting
    # a pre-sorted array favors insertion sort.[4]
    print(f"Generating master array (N={N_SIZE})...", file=sys.stderr)
    original_data = generate_random_array(N_SIZE)
    
    results = {}  # Stores {k: min_time}

    print(f"Benchmarking k from 1 to {K_MAX}...", file=sys.stderr)

    for k in range(1, K_MAX + 1):
        run_times = []
        
        for i in range(NUM_RUNS):
            # 1. Create a fresh copy of the *original* unsorted data [4]
            data_copy = original_data[:]
            
            # 2. Disable Garbage Collection during the timed section [5]
            gc.disable()
            
            start_time = time.perf_counter()
            hybrid_merge_sort(data_copy, 0, N_SIZE - 1, k)
            end_time = time.perf_counter()
            
            if not is_sorted(data_copy):
                print(f"CRITICAL ERROR: Sort failed for k={k}")
                raise RuntimeError(f"Sort verification failed for k={k}")

            gc.enable()
            
            run_times.append(end_time - start_time)
        
        # We take the *minimum* time, as it's least likely to be
        # affected by OS interrupts or other background noise.[4]
        min_time = min(run_times)
        results[k] = min_time
        print(f"  k = {k:2d}, min_time = {min_time:8.4f}s", file=sys.stderr)

    optimal_k = min(results, key=results.get)
    
    print(f"--- Complete ---", file=sys.stderr)
    print(f"Optimal k: {optimal_k} (Time: {results[optimal_k]:.4f}s)", file=sys.stderr)
    
    return optimal_k

# Part 3: Main Execution

if __name__ == "__main__":
    optimal_k_value = find_optimal_k()
    print(optimal_k_value)