import math
import random
import time
import gc

# Part 1: Algorithms Implementations From Book
class HybridSorter:
    @classmethod
    def INSETION_SORT(self, A, p, r):
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

    @classmethod
    def MERGE(self, A, p, q, r):
        """
        Merges the two sorted subarrays A[p..q] and A[q+1..r].
        From page 25 in the book 
        Note we use 0 indexed arrays.
        """
        n1 = q - p + 1
        n2 = r - q 
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

    @classmethod
    def hybrid_merge_sort(self, A, p, r, k):
        """
        Sorts the subarray A[p..r] (inclusive) using the hybrid algorithm     
        It uses Insertion Sort for subarrays of size 'k' or less.
        """
        n = r - p + 1
        
        if n <= k:
            # Switch to insertion_sort for this small subarray
            HybridSorter.INSETION_SORT(A, p, r)
        elif p < r:
            # If the subarray is larger than k, divide and conquer as usual.
            q = (p + r) // 2
            HybridSorter.hybrid_merge_sort(A, p, q, k)
            HybridSorter.hybrid_merge_sort(A, q + 1, r, k)
            HybridSorter.MERGE(A, p, q, r)


# Part 2 helper functions

def generate_sorted_array(n):
    return list(range(n))

def generate_sorted_array_reversed(n):
    arr = generate_sorted_array(n)
    arr.reverse()
    return arr

def generate_random_array(n):
    """generate random array with different numbers"""
    arr = generate_sorted_array(n)
    random.shuffle(arr)
    return arr

def generate_nearly_sorted_array(n, k_swaps):
    """return sorted array up to k_swaps"""
    arr = generate_sorted_array(n)
    for _ in range(k_swaps):
        i = random.randrange(n)
        j = random.randrange(n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def is_sorted(A):
    """Helper function to check if an array is sorted."""
    return A == sorted(A)


# Part 3: Empirical Benchmark to Find Optimal K

def time_hybrid_sort(A, k):
    """run hybrid merge sort and return the time it took"""
    gc.disable()
    start_time = time.perf_counter()
    HybridSorter.hybrid_merge_sort(A, 0, len(A) - 1, k)
    end_time = time.perf_counter()
    gc.enable()
    
    if not is_sorted(A):
        print(f"CRITICAL ERROR: Sort failed for k={k}")
        raise RuntimeError(f"Sort verification failed for k={k}")
    
    return end_time - start_time

def find_optimal_k_given_array(A, k_list, RUNS_PER_K=10):
    """for a specific array A and 

    Args:
        A: array of different integers
        k_list: list of k values to check
        RUNS_PER_K: how many times should each k value be tested
    """
    results = {}

    for k in k_list:
        # take the avrage run time over {RUNS_PER_K} runs
        run_times = []
        for _ in range(RUNS_PER_K):
            A_copy = A[:]
            run_time = time_hybrid_sort(A=A_copy, k=k)
            run_times.append(run_time)
        avg_time = sum(run_times) / len(run_times)
        results[k] = avg_time
    return results

def run_experiment(n_list, k_list, input_type_name, data_generator):
    """generate an array based on some specified peridaigm of length n 
    and find the optimal k value for specified array
    Args:
        n_list: list of n values to test
        k_list: list of k values to tset
        input_type_name: title
        data_generator: function that returns an array
    """
    print(f"\n--- Running Experiment: {input_type_name} Inputs ---")
    results = {}

    for n in n_list:
        print(f"Processing for n = {n}...")
        results[n] = {}
        
        original_data = []
        if input_type_name == "Nearly Sorted":
            original_data = data_generator(n, n // 10)
        else:
            original_data = data_generator(n)
        
        result = find_optimal_k_given_array(original_data, k_list, RUNS_PER_K=5)
        optimal_k = min(result, key=result.get)
        results[n] = {optimal_k: result[optimal_k]} 
        print(f"n = {n}, best k = {optimal_k} at {result[optimal_k]:.4f}s")

    return results


# Part 4: Main Execution

if __name__ == "__main__":
    N_VALUES =  [100,500,1000,5000,10000] 
    K_VALUES = list(range(10, 60))

    random_results1 = run_experiment(N_VALUES, K_VALUES, "Random1", generate_random_array)
    random_results2 = run_experiment(N_VALUES, K_VALUES, "Random2", generate_random_array)
    random_results3 = run_experiment(N_VALUES, K_VALUES, "Random3", generate_random_array)
    nearly_sorted_results = run_experiment(N_VALUES, K_VALUES, "Nearly Sorted", generate_nearly_sorted_array)
    sorted_results = run_experiment(N_VALUES, K_VALUES, "Sorted", generate_sorted_array)
    reversed_sorted_results = run_experiment(N_VALUES, K_VALUES, "Sorted Reversed", generate_sorted_array_reversed)
