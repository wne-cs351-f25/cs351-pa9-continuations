"""
Threads vs Processes in Python
Demonstrates the differences and when to use each

Key Concepts:
- Shared memory (threads) vs. isolated memory (processes)
- The Global Interpreter Lock (GIL)
- CPU-bound vs. I/O-bound tasks
"""

import threading
import multiprocessing
import time
import os

print("=" * 60)
print("PART 1: Understanding Threads vs Processes")
print("=" * 60)


def print_info(name):
    """Print process and thread information"""
    print(f"{name}:")
    print(f"  Process ID: {os.getpid()}")
    print(f"  Thread ID: {threading.get_ident()}")
    print()


# Main thread
print_info("Main thread")

print("\n" + "=" * 60)
print("PART 2: Shared Memory with Threads")
print("=" * 60)

# Shared mutable state (dangerous with threads!)
counter = {"value": 0}


def increment_shared(n):
    """Increment shared counter (not thread-safe!)"""
    for _ in range(n):
        counter["value"] += 1


def increment_shared_safe(n, lock):
    """Increment shared counter with lock (thread-safe)"""
    for _ in range(n):
        with lock:
            counter["value"] += 1


# Demonstration without lock (may have race conditions)
print("WITHOUT lock:")
counter["value"] = 0
threads = []
for _ in range(5):
    t = threading.Thread(target=increment_shared, args=(1000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Expected: 5000, Got: {counter['value']}")
if counter["value"] != 5000:
    print("⚠️  Race condition! Multiple threads modified shared state unsafely")

# Demonstration with lock
print("\nWITH lock:")
counter["value"] = 0
lock = threading.Lock()
threads = []
for _ in range(5):
    t = threading.Thread(target=increment_shared_safe, args=(1000, lock))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Expected: 5000, Got: {counter['value']}")
print("✓ Lock prevents race conditions")

print("\n" + "=" * 60)
print("PART 3: Isolated Memory with Processes")
print("=" * 60)


def increment_process(n):
    """Each process has its own memory space"""
    global counter
    counter = {"value": 0}  # This is a SEPARATE counter per process
    for _ in range(n):
        counter["value"] += 1
    print(f"Process {os.getpid()}: counter = {counter['value']}")


print("Starting processes (each has isolated memory):")
processes = []
for _ in range(3):
    p = multiprocessing.Process(target=increment_process, args=(100,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()

print(f"Main process counter: {counter['value']}")
print("Note: Main process counter unchanged! Processes don't share memory.")

print("\n" + "=" * 60)
print("PART 4: The Global Interpreter Lock (GIL)")
print("=" * 60)


def cpu_bound_task(n):
    """CPU-intensive task (affected by GIL)"""
    count = 0
    for i in range(n):
        count += i * i
    return count


def io_bound_task(n):
    """I/O-intensive task (not affected by GIL)"""
    time.sleep(n * 0.001)  # Simulate I/O wait
    return n


# CPU-bound with threads (GIL limits parallelism)
print("CPU-bound task with THREADS:")
start = time.time()
threads = []
for _ in range(4):
    t = threading.Thread(target=cpu_bound_task, args=(1_000_000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
thread_time = time.time() - start
print(f"Time with threads: {thread_time:.2f}s")

# CPU-bound with processes (true parallelism)
print("\nCPU-bound task with PROCESSES:")
start = time.time()
processes = []
for _ in range(4):
    p = multiprocessing.Process(target=cpu_bound_task, args=(1_000_000,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
process_time = time.time() - start
print(f"Time with processes: {process_time:.2f}s")

speedup = thread_time / process_time
print(f"\nSpeedup: {speedup:.2f}x")
print("Note: Processes are MUCH faster for CPU-bound tasks due to GIL")

print("\n" + "=" * 60)
print("PART 5: When to Use Threads vs Processes")
print("=" * 60)

print(
    """
Use THREADS when:
-----------------
✓ I/O-bound tasks (network, file operations)
✓ Need shared memory
✓ Lower overhead (threads are lighter than processes)
✓ GIL is released during I/O operations

Example: Web scraping, database queries, file processing


Use PROCESSES when:
-------------------
✓ CPU-bound tasks (computations, data processing)
✓ Need true parallelism
✓ Want isolation (no shared state)
✓ Each task is independent

Example: Image processing, scientific computing, video encoding


The GIL Problem:
----------------
- Only ONE thread can execute Python bytecode at a time
- Other threads must wait for the GIL
- CPU-bound tasks get NO speedup from threads
- I/O-bound tasks release GIL during I/O, so threads help

Why did the GIL exist?
- Simplifies memory management (reference counting)
- Makes C extensions easier to write
- Single-threaded programs run faster
"""
)

print("\n" + "=" * 60)
print("PART 6: Modern Alternatives")
print("=" * 60)

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def task(n):
    """Simple task for demonstration"""
    return n * n


print("Using ThreadPoolExecutor:")
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(task, range(10))
    print(f"Results: {list(results)}")

print("\nUsing ProcessPoolExecutor:")
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(task, range(10))
    print(f"Results: {list(results)}")

print(
    """
concurrent.futures provides a high-level interface:
- ThreadPoolExecutor for I/O-bound tasks
- ProcessPoolExecutor for CPU-bound tasks
- Unified API for both
- Easy to switch between threading and multiprocessing
"""
)

print("\n" + "=" * 60)
print("CONNECTION TO LANGUAGE DESIGN")
print("=" * 60)

print(
    """
Concurrency Models in Different Languages:
------------------------------------------

Python (with GIL):
- Global lock for thread safety
- Simple memory management
- Limited CPU parallelism
- Good for I/O concurrency

Java/C#:
- True multi-threading
- More complex memory model
- Better CPU parallelism
- Need explicit synchronization

Go:
- Goroutines (lightweight threads)
- Channels for communication
- "Don't communicate by sharing memory; share memory by communicating"
- Built-in concurrency primitives

Rust:
- Ownership system prevents data races at COMPILE TIME
- "Fearless concurrency"
- No runtime overhead
- Type system enforces thread safety

Key Design Tradeoff:
- Safety vs. Performance vs. Simplicity
- Python chose simplicity (GIL)
- Now removing it in Python 3.13+ for performance
"""
)
