"""
Python's GIL Evolution: From Bottleneck to Optional

This demonstrates the history of the GIL and Python 3.13+'s free-threading mode
Based on PEP 703: Making the Global Interpreter Lock Optional
"""

import sys
import threading
import time

print("=" * 60)
print("PYTHON VERSION INFORMATION")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Python version info: {sys.version_info}")

# Check if running with free-threading (Python 3.13+)
has_gil = True
try:
    # In Python 3.13+ with --disable-gil, this attribute exists
    has_gil = sys._is_gil_enabled()
    print(f"GIL enabled: {has_gil}")
except AttributeError:
    print("GIL status: Always enabled (Python < 3.13)")

print("\n" + "=" * 60)
print("PART 1: Why Did the GIL Exist?")
print("=" * 60)

print(
    """
Historical Context:
-------------------
1. Reference Counting Memory Management
   - CPython uses reference counting for garbage collection
   - Every object has a refcount: how many references point to it
   - When refcount reaches 0, memory is freed
   - Problem: refcount updates aren't atomic!

2. Thread Safety Challenge
   - Without GIL: Multiple threads could update refcount simultaneously
   - Race condition example:

     Thread 1: Read refcount (5) → Increment (6) → Write back
     Thread 2: Read refcount (5) → Increment (6) → Write back
     Result: Refcount is 6, should be 7! Memory leak or premature free!

3. The GIL Solution
   - One global lock for ALL Python bytecode execution
   - Only one thread executes Python code at a time
   - Prevents refcount race conditions
   - Simple, but limits parallelism

4. Why Not Per-Object Locks?
   - Would need locks on EVERY object (millions!)
   - Lock acquisition/release overhead
   - Deadlock possibilities
   - Complexity in C API
"""
)

print("\n" + "=" * 60)
print("PART 2: Demonstrating GIL Impact")
print("=" * 60)


def demonstrate_gil_contention():
    """Show how GIL limits CPU parallelism"""

    def cpu_work(n, name):
        """Pure CPU work"""
        start = time.time()
        total = 0
        for i in range(n):
            total += i**2
        elapsed = time.time() - start
        print(f"{name}: {elapsed:.3f}s")
        return total

    # Single-threaded baseline
    print("Single-threaded (baseline):")
    start = time.time()
    cpu_work(5_000_000, "Task 1")
    cpu_work(5_000_000, "Task 2")
    sequential_time = time.time() - start
    print(f"Total time: {sequential_time:.3f}s\n")

    # Multi-threaded (limited by GIL)
    print("Multi-threaded (with GIL):")
    start = time.time()
    t1 = threading.Thread(target=cpu_work, args=(5_000_000, "Thread 1"))
    t2 = threading.Thread(target=cpu_work, args=(5_000_000, "Thread 2"))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    threaded_time = time.time() - start
    print(f"Total time: {threaded_time:.3f}s")

    speedup = sequential_time / threaded_time
    print(f"\nSpeedup: {speedup:.2f}x (expected ~2x without GIL, got ~1x with GIL)")

    if speedup < 1.5:
        print("⚠️  GIL prevents parallel execution!")


demonstrate_gil_contention()

print("\n" + "=" * 60)
print("PART 3: PEP 703 - Making the GIL Optional")
print("=" * 60)

print(
    """
Python 3.13+ Free-Threading Mode:
----------------------------------

Building Python with --disable-gil:
    ./configure --disable-gil
    make

Or using environment variable:
    PYTHON_GIL=0 python script.py

Changes Required:
-----------------
1. Biased Reference Counting
   - Objects track which thread owns them
   - Local references don't need synchronization
   - Only shared objects need atomic operations

2. Immortal Objects
   - Common objects (None, True, False, small ints) made immortal
   - Refcount never changes
   - No synchronization needed

3. Per-Object Locks
   - Fine-grained locking on mutable objects
   - Lock-free algorithms where possible
   - Reduced contention

4. Thread-Safe Core Data Structures
   - dict, list, set reimplemented with thread safety
   - Mimalloc memory allocator (thread-local pools)

Performance Impact:
-------------------
Single-threaded: ~5-10% slower (overhead of thread safety)
Multi-threaded:  Up to Nx speedup on N cores (CPU-bound)

Compatibility:
--------------
- Pure Python: Mostly compatible
- C Extensions: May need updates for thread safety
- Existing code: Runs unchanged (with safety overhead)
"""
)

print("\n" + "=" * 60)
print("PART 4: Practical Example - Before and After")
print("=" * 60)


def parallel_computation(data, num_threads):
    """Simulate parallel computation"""

    def worker(chunk, results, index):
        result = sum(x * x for x in chunk)
        results[index] = result

    chunk_size = len(data) // num_threads
    threads = []
    results = [0] * num_threads

    start = time.time()

    for i in range(num_threads):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < num_threads - 1 else len(data)
        chunk = data[start_idx:end_idx]

        t = threading.Thread(target=worker, args=(chunk, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    return sum(results), elapsed


data = list(range(1_000_000))

print("Computing sum of squares...")
result_1, time_1 = parallel_computation(data, 1)
result_4, time_4 = parallel_computation(data, 4)

print(f"1 thread:  {time_1:.3f}s")
print(f"4 threads: {time_4:.3f}s")
print(f"Speedup:   {time_1/time_4:.2f}x")

if has_gil:
    print("\n⚠️  With GIL: Limited speedup (~1x)")
    print("   To see true parallelism, run with Python 3.13+ --disable-gil")
else:
    print("\n✓ Free-threading: True parallelism! (~4x on 4 cores)")

print("\n" + "=" * 60)
print("PART 5: Migration Considerations")
print("=" * 60)

print(
    """
Should You Use Free-Threading?
-------------------------------

YES, if:
✓ CPU-bound workloads
✓ Pure Python code
✓ Can tolerate 5-10% single-thread overhead
✓ Want to avoid multiprocessing overhead
✓ Need shared memory between parallel tasks

NO, if:
✗ Primarily I/O-bound (threads already work well)
✗ Heavy use of C extensions (may not be thread-safe)
✗ Single-threaded performance critical
✗ Need maximum compatibility

Best Practices:
---------------
1. Test with both modes (GIL enabled/disabled)
2. Use thread-safe data structures (queue.Queue, threading.Lock)
3. Minimize shared mutable state
4. Consider using concurrent.futures for abstraction
5. Profile before optimizing

Timeline:
---------
- Python 3.13 (Oct 2024): Experimental free-threading support
- Python 3.14 (Oct 2025): Improved performance and stability
- Python 4.0 (?): GIL disabled by default?
"""
)

print("\n" + "=" * 60)
print("PART 6: Comparison with Other Languages")
print("=" * 60)

print(
    """
How Different Languages Handle Concurrency:
-------------------------------------------

Python (with GIL):
    Pros: Simple, safe for single-threaded
    Cons: Limited parallelism for CPU tasks
    Model: Global lock

Python (free-threading):
    Pros: True parallelism, shared memory
    Cons: Small single-thread overhead
    Model: Per-object locks + biased refcounting

Java:
    Pros: True multi-threading, mature tooling
    Cons: Complex memory model, need explicit sync
    Model: No GIL, synchronized blocks

Go:
    Pros: Lightweight goroutines, channels
    Cons: Potential deadlocks, race conditions
    Model: CSP (Communicating Sequential Processes)

Rust:
    Pros: Thread safety at compile time!
    Cons: Steep learning curve
    Model: Ownership + type system guarantees

Node.js:
    Pros: Event loop, non-blocking I/O
    Cons: CPU tasks block event loop
    Model: Single-threaded + worker threads
"""
)

print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)

print(
    """
1. GIL was a DESIGN CHOICE - simplicity over parallelism
2. PEP 703 makes GIL optional in Python 3.13+
3. Free-threading enables true CPU parallelism
4. Trade-off: Small single-thread overhead for better scaling
5. Different languages make different concurrency trade-offs
6. No "perfect" solution - depends on use case

Understanding the GIL helps you:
- Choose the right concurrency model
- Design better parallel programs
- Appreciate language design trade-offs
- Make informed technology choices
"""
)
