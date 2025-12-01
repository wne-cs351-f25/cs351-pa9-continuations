# PA9: Modern Language Features - Python Deep Dive

**Due:** December 7, 2024
**Topics:** Pass-by-object-reference, Duck typing, OBJ to Python synthesis, Language Design (GIL)

## Overview

Throughout this course, we've built interpreters for increasingly sophisticated programming languages using PLCC. Implementing:

- Lexical analysis and parsing (PA1-PA2)
- Expression evaluation and environments (PA3-PA4)
- Procedures and closures (PA5)
- Parameter passing mechanisms (PA6)
- Type checking (PA7)
- Object-oriented features (PA8)

Now it's time to study a production programming language (Python) and understand how it implements these features, with special attention to its unique approaches and recent evolution.

## Learning Objectives

By completing this assignment, you will:

1. Understand Python's pass-by-object-reference mechanism and how it differs from pass-by-value/reference.
2. Appreciate duck typing and compare it to static type checking.
3. Synthesize object-oriented concepts by translating OBJ language code to Python.
4. Analyze language design trade-offs through the lens of Python's GIL evolution.
5. Connect real-world language design decisions to the theoretical concepts from the course.

## Prerequisites

- Completion of PA6 (Parameter Passing)
- Completion of PA7 (Type Checking)
- Completion of PA8 (Classes and Objects)
- Python 3.10+ installed (Python 3.13+ recommended for GIL experiments)

## Assignment Structure

This assignment has four core parts and one bonus opportunity:

### Part 1: Pass-by-Object-Reference (25 points)

**Background:** In PA6, we used call-by-value, call-by-reference, call-by-name, and call-by-need. Python uses a different model: pass-by-object-reference.

**Tasks:**

1. **Experimentation (10 points)**

   - Run `01-pass-by-object-reference.py` and observe the output.
   - Modify the examples to test edge cases:
     - What happens with tuples? (immutable)
     - What happens with dictionaries? (mutable)
     - What about nested data structures?

2. **Analysis (10 points)**
   Write a short report (300-500 words) answering:

   - How is pass-by-object-reference different from pass-by-value?
   - How is it different from pass-by-reference?
   - Why does Python's approach make sense for its design goals?
   - What are potential pitfalls for programmers coming from Java or C++?

3. **Implementation (5 points)**
   Create a function `safe_append(lst, item)` that appends an item to a list WITHOUT modifying the original list. Test it with:
   ```python
   original = [1, 2, 3]
   result = safe_append(original, 4)
   assert original == [1, 2, 3]
   assert result == [1, 2, 3, 4]
   ```

**Deliverable:** `part1_analysis.md` and `part1_code.py`

---

### Part 2: Duck Typing vs Static Typing (25 points)

**Background:** In PA7, you used a type checker for TYPE0/TYPE1 languages with static type checking. Python uses duck typing: "If it walks like a duck and quacks like a duck, it must be a duck."

**Tasks:**

1. **Comparison Study (10 points)**

   - Run `02-duck-typing.py` and analyze the examples.
   - Compare the OBJ language class hierarchy to Python's duck typing.
   - Identify situations where duck typing is more flexible.
   - Identify situations where static typing catches more errors.

2. **Protocol Implementation (10 points)**
   Implement a file processing system that works with multiple "file-like" objects:

   - `StringFile`: Stores content in a string.
   - `ListFile`: Stores content as list of lines.
   - `CountingFile`: Wraps another file and counts operations.

   All should work with this function:

   ```python
   def process_file(file_like):
       file_like.write("Header\n")
       file_like.write("Content\n")
       file_like.write("Footer\n")
       return file_like.read()
   ```

3. **Type Hints (5 points)**
   Add type hints to your implementation using `Protocol` from `typing`. Use `mypy` to verify type correctness.

**Deliverable:** `part2_analysis.md` and `part2_code.py`

---

### Part 3: OBJ to Python Translation (30 points)

**Background:** In PA8, you used the OBJ language. Now you will see how those concepts translate to Python.

**Tasks:**

1. **Translation (15 points)**
   Translate 3 distinct PA8 programs (or provided OBJ examples) to Python. You can use examples like:

   - A simple class hierarchy (e.g., Shapes)
   - A recursive data structure (e.g., Lists or Trees)
   - An example using `super` or `this`

   For each translation:

   - Include the original OBJ code (as comments or separate files).
   - Write the equivalent Python code.
   - Demonstrate that they produce equivalent behavior/output.

2. **Analysis (15 points)**
   For each of your 3 translations, explain the syntax and semantic differences.
   - How does Python handle `this` vs OBJ?
   - How is inheritance declared?
   - How are fields initialized?
   - Write a reflection (1-2 paragraphs) on Object-Oriented Programming in both languages.

**Deliverable:** `part3_translation.py` (containing the 3 examples) and `part3_analysis.md`

---

### (Optional) Part 4: Language Design Synthesis (20 points)

**Background:** Python's Global Interpreter Lock (GIL) has been a defining feature and limitation. Python 3.13 introduces optional free-threading mode (PEP 703).

**Tasks:**

1. **GIL Evolution Study (10 points)**

   - Read/Run `04-python-gil-evolution.py`.
   - **Crucial:** Run this with the special free-threaded Python build included in the devcontainer:
     ```bash
     python-free 04-python-gil-evolution.py
     ```
   - Answer the following questions:
     - Why did Python originally have a GIL?
     - What specific problems does it solve?
     - How does PEP 703 address the "GIL problem"?

2. **Design Reflection (10 points)**
   Write a short essay (2-3 paragraphs) on language design trade-offs, connecting to course themes (simplicity vs performance, safety vs flexibility).
   - Discuss why a language might choose _simplicity_ (like Python's original GIL) over _performance_.
   - Discuss how Python is now shifting that trade-off and what the costs might be (compatibility, complexity).

**Deliverable:** `part4_analysis.md`

---

### (Optional) Bonus: Threads vs Processes (10 extra credit)

**Background:** Concurrency models are crucial for modern programming.

**Task:**
Implement and benchmark a "Threads vs Processes" demo.

- Create a CPU-bound task (e.g., calculating primes).
- Run it sequentially.
- Run it using `threading`.
- Run it using `multiprocessing`.
- Measure the execution times and explain the results.
- (Optional) Visualize the results.

**Deliverable:** `bonus_concurrency.py` and `bonus_report.md`

---

## Submission

**To Submit:**

1. Test your programs to ensure they work correctly
2. From inside your container: `tar -czf /workspace/pa9-YOURNAME.zip /workspace`
3. Download and submit the zip file to Kodiak

**Grading Criteria:**

- **Submission (33.3%):** Files are properly named and located as specified
- **Completeness (33.3%):** All questions attempted (incomplete = incorrect)
- **Correctness (33.3%):** Solutions demonstrate understanding of type systems

**Late Policy:** 10% per day, maximum 5 days late

---

## Resources

### Required Reading

- PEP 703: Making the Global Interpreter Lock Optional
  https://peps.python.org/pep-0703/
- Python Data Model documentation
  https://docs.python.org/3/reference/datamodel.html

### Tools

- `mypy`: Static type checker for Python
  ```bash
  pip install mypy
  mypy your_code.py
  ```

---

_Course content developed by Declan Gray-Mullen for WNEU with Gemini_
