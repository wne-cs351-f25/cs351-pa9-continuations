"""
OBJ Language to Python: Side-by-Side Comparison

This file demonstrates how concepts from PLCC's OBJ language
translate to Python, connecting to previous course assignments.
"""

print("=" * 70)
print("OBJ LANGUAGE vs PYTHON: A COMPREHENSIVE COMPARISON")
print("=" * 70)

print(
    """
Throughout this course, we've built interpreters for increasingly
sophisticated languages using PLCC. Now we'll see how a production
language (Python) implements similar features.
"""
)

print("\n" + "=" * 70)
print("PART 1: Classes and Objects")
print("=" * 70)

print(
    """
OBJ Language (PLCC):
--------------------
class Point
  field x
  field y
  method init = proc(x_val, y_val)
    { set <this>x = x_val
    ; set <this>y = y_val
    ; this
    }
  method distance = proc()
    let
      x_sq = *(x, x)
      y_sq = *(y, y)
    in
      +(x_sq, y_sq)  % simplified: should be sqrt
end

define p = new Point
.<p>init(3, 4)
.<p>distance()


Python Equivalent:
------------------
"""
)


class Point:
    """A point in 2D space"""

    def __init__(self, x_val, y_val):
        """Constructor (like init method in OBJ)"""
        self.x = x_val  # field x
        self.y = y_val  # field y

    def distance(self):
        """Calculate distance from origin"""
        x_sq = self.x * self.x
        y_sq = self.y * self.y
        return x_sq + y_sq  # Simplified


p = Point(3, 4)
print(f"Point: ({p.x}, {p.y})")
print(f"Distance²: {p.distance()}")

print(
    """
Key Differences:
- Python: __init__ is constructor (automatic)
- OBJ: init is manual method, returns this
- Python: self is implicit in method calls
- OBJ: <this> is explicit
- Python: . for both field access and method calls
- OBJ: . for methods, <obj>field for direct access
"""
)

print("\n" + "=" * 70)
print("PART 2: Inheritance")
print("=" * 70)

print(
    """
OBJ Language:
-------------
class Shape
  method area = proc() 0
end

class Rectangle extends Shape
  field width
  field height
  method init = proc(w, h)
    { set <this>width = w
    ; set <this>height = h
    ; this
    }
  method area = proc()
    *(width, height)
end

class Circle extends Shape
  field radius
  method init = proc(r)
    { set <this>radius = r
    ; this
    }
  method area = proc()
    *(radius, radius)  % simplified: should be π*r²
end


Python Equivalent:
------------------
"""
)


class Shape:
    """Base class for shapes"""

    def area(self):
        return 0


class Rectangle(Shape):
    """Rectangle extending Shape"""

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def area(self):
        """Override parent's area method"""
        return self.width * self.height


class Circle(Shape):
    """Circle extending Shape"""

    def __init__(self, r):
        self.radius = r

    def area(self):
        """Override parent's area method"""
        return self.radius * self.radius  # Simplified


shapes = [Rectangle(5, 10), Circle(7), Rectangle(3, 4)]

print("Shapes and their areas:")
for i, shape in enumerate(shapes, 1):
    print(f"  Shape {i}: area = {shape.area()}")

print(
    """
Key Similarities:
- Both support single inheritance
- Both have method overriding
- Both use dynamic dispatch
"""
)

print("\n" + "=" * 70)
print("PART 3: Static vs Instance Members")
print("=" * 70)

print(
    """
OBJ Language:
-------------
class Counter
  static count = 0
  field id
  method init = proc()
    { set <Counter>count = add1(<Counter>count)
    ; set <this>id = <Counter>count
    ; this
    }
end

define c1 = .<new Counter>init()  % id = 1, count = 1
define c2 = .<new Counter>init()  % id = 2, count = 2


Python Equivalent:
------------------
"""
)


class Counter:
    """Counter with static count"""

    count = 0  # Class variable (static)

    def __init__(self):
        Counter.count += 1
        self.id = Counter.count  # Instance variable (field)


c1 = Counter()
c2 = Counter()
c3 = Counter()

print(f"c1.id = {c1.id}, c2.id = {c2.id}, c3.id = {c3.id}")
print(f"Counter.count = {Counter.count}")

print(
    """
Key Points:
- OBJ: 'static' keyword for class-level variables
- Python: Variables defined in class body are class variables
- Both: Instance variables are per-object
- Access: <ClassName>var (OBJ) vs ClassName.var (Python)
"""
)

print("\n" + "=" * 70)
print("PART 4: Mutation and References")
print("=" * 70)

print(
    """
Connection to PA6 (Parameter Passing):
- Call-by-value: Copies are passed
- Call-by-reference: References are passed, mutation affects original
- Call-by-object-reference (Python): References passed, effect depends on mutability
"""
)


class MutableBox:
    def __init__(self, value):
        self.value = value


def modify_box(box, new_value):
    """Modifies the box (like call-by-reference)"""
    box.value = new_value


def replace_box(box, new_value):
    """Tries to replace the box (doesn't affect caller)"""
    box = MutableBox(new_value)  # Rebinds local name


box1 = MutableBox(10)
print(f"Before modify: box1.value = {box1.value}")
modify_box(box1, 20)
print(f"After modify:  box1.value = {box1.value}")

box2 = MutableBox(30)
print(f"\nBefore replace: box2.value = {box2.value}")
replace_box(box2, 40)
print(f"After replace:  box2.value = {box2.value}")

print(
    """
In OBJ:
    set <loc>var = exp   % Mutation

In Python:
    obj.attr = value     % Mutation
    obj = new_value      % Rebinding (local only)
"""
)

print("\n" + "=" * 70)
print("PART 5: Type Systems")
print("=" * 70)

print(
    """
Connection to PA7 (Type Checker):
- TYPE0/TYPE1: Static type checking
- Python: Dynamic typing with optional type hints

OBJ/PLCC (Static Typing):
-------------------------
In a typed version:
    proc<int -> int> square = proc(x : int) : int {
        *(x, x)
    }

Type checking at PARSE time:
- Catches errors early
- More restrictive
- Better tooling


Python (Dynamic Typing):
------------------------
"""
)


def square(x):
    """Works with any type that supports multiplication"""
    return x * x


print(f"square(5) = {square(5)}")
print(f"square(3.14) = {square(3.14)}")
print(f"square('ha') = {square('ha')}")

print(
    """
With type hints (optional):
"""
)

from typing import Union


def typed_square(x: Union[int, float]) -> Union[int, float]:
    """Type hints provide documentation and static checking"""
    return x * x


print(f"typed_square(5) = {typed_square(5)}")
print(f"typed_square(3.14) = {typed_square(3.14)}")
# typed_square('ha') would be flagged by mypy, but runs fine!

print(
    """
Key Difference:
- PLCC: Types enforced at compile/check time
- Python: Types are hints, checked by external tools (mypy)
- Python: Runtime checks are dynamic
"""
)

print("\n" + "=" * 70)
print("PART 6: Closures and Environments")
print("=" * 70)

print(
    """
Connection to PA4/PA5 (Environments):

OBJ:
----
let
  x = 10
in
  let
    f = proc(y) +(x, y)
  in
    .f(5)  % Returns 15, f captures x

Environment chain:
    f's env → let's env (x=10) → global env
"""
)


def make_adder(x):
    """Returns a closure that adds x to its argument"""

    def adder(y):
        return x + y  # Captures x from enclosing scope

    return adder


add_10 = make_adder(10)
print(f"add_10(5) = {add_10(5)}")
print(f"add_10(20) = {add_10(20)}")

print(
    """
Python's LEGB Rule (Environment Chain):
- Local: Current function
- Enclosing: Outer functions
- Global: Module level
- Built-in: Python built-ins

Same concept as environment chains in PLCC!
"""
)

print("\n" + "=" * 70)
print("PART 7: Summary - Course Concepts in Python")
print("=" * 70)

print(
    """
┌─────────────────────┬────────────────────┬──────────────────────────┐
│ Course Assignment   │ Concept            │ Python Implementation    │
├─────────────────────┼────────────────────┼──────────────────────────┤
│ PA1 - Lexical       │ Tokens             │ Python tokenizer         │
│ PA2 - Syntax        │ Grammar            │ Python parser (AST)      │
│ PA3 - Interpreter   │ Evaluation         │ Python interpreter       │
│ PA4 - Environments  │ Variable scope     │ LEGB rule                │
│ PA5 - Procedures    │ Closures           │ Nested functions         │
│ PA6 - Parameters    │ Passing mechanisms │ Pass-by-object-reference │
│ PA7 - Type Checker  │ Static types       │ Dynamic + type hints     │
│ PA8 - Classes       │ OOP features       │ Class/inheritance        │
│ PA9 - Python!       │ Real language      │ All of the above         │
└─────────────────────┴────────────────────┴──────────────────────────┘

You've built all these features from scratch in PLCC!
Now you understand how Python implements them.

Language Design Insights:
-------------------------
1. Syntax: Python chose simplicity (significant whitespace)
2. Semantics: Dynamic typing for flexibility
3. Memory: Reference counting + GC
4. Concurrency: GIL for simplicity → free-threading for performance
5. Objects: Everything is an object
6. Philosophy: "There should be one-- and preferably only one --obvious way to do it"

Trade-offs:
-----------
- Simplicity vs. Performance (GIL)
- Flexibility vs. Safety (dynamic typing)
- Readability vs. Verbosity (explicit self)
- Compatibility vs. Innovation (GIL removal)

Every language makes different choices based on its goals and constraints!
"""
)
