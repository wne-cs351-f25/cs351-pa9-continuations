"""
Duck Typing in Python
"If it walks like a duck and quacks like a duck, it's a duck"

Connection to PA7: Compare with static type checking in TYPE0/TYPE1
"""

print("=" * 60)
print("PART 1: Duck Typing Basics")
print("=" * 60)


class Duck:
    def quack(self):
        return "Quack!"

    def walk(self):
        return "Waddle waddle"


class Person:
    def quack(self):
        return "I'm imitating a duck: Quack!"

    def walk(self):
        return "Walking on two legs"


class Dog:
    def bark(self):
        return "Woof!"

    def walk(self):
        return "Walking on four legs"


def make_it_quack(thing):
    """
    This function doesn't care about the TYPE of 'thing'
    It only cares if 'thing' HAS a quack() method

    In TYPE0/TYPE1 (PA7), we would need explicit type declarations
    """
    return thing.quack()


duck = Duck()
person = Person()

print(f"Duck quacks: {make_it_quack(duck)}")
print(f"Person quacks: {make_it_quack(person)}")
print("\nBoth work! Python doesn't check types at compile time.")

print("\nWhat about Dog?")
dog = Dog()
try:
    print(f"Dog quacks: {make_it_quack(dog)}")
except AttributeError as e:
    print(f"Error: {e}")
    print("Dog doesn't have quack(), so it fails at RUNTIME")

print("\n" + "=" * 60)
print("PART 2: Polymorphism without Inheritance")
print("=" * 60)


class FileWriter:
    def __init__(self, filename):
        self.filename = filename
        self.content = []

    def write(self, text):
        self.content.append(text)

    def save(self):
        with open(self.filename, "w") as f:
            f.writelines(self.content)


class ConsoleWriter:
    def write(self, text):
        print(f"[Console] {text}", end="")


class ListWriter:
    def __init__(self):
        self.items = []

    def write(self, text):
        self.items.append(text)


def write_report(writer, data):
    """
    Works with ANY object that has a write() method
    No inheritance required!

    Compare to OBJ language where we'd use class inheritance
    """
    writer.write("=== REPORT ===\n")
    for item in data:
        writer.write(f"- {item}\n")
    writer.write("=== END ===\n")


# All these work with the same function!
data = ["Item 1", "Item 2", "Item 3"]

print("Writing to console:")
console = ConsoleWriter()
write_report(console, data)

print("\nWriting to list:")
list_writer = ListWriter()
write_report(list_writer, data)
print(f"List contents: {list_writer.items}")

print("\n" + "=" * 60)
print("PART 3: Duck Typing vs Static Typing")
print("=" * 60)

print(
    """
In TYPE0/TYPE1 (PA7), you might write:

    proc<int -> int> square = proc(x : int) : int {
        *(x, x)
    }

Type checking happens at PARSE/CHECK time (static)
- Catches type errors before running
- More restrictive
- Better tooling support

In Python with duck typing:

    def square(x):
        return x * x

Type checking happens at RUNTIME (dynamic)
- More flexible (works with int, float, complex, numpy arrays...)
- Errors only appear when code runs
- Relies on protocols/interfaces
"""
)


def square(x):
    """Works with anything that supports multiplication"""
    return x * x


print(f"square(5) = {square(5)}")
print(f"square(3.14) = {square(3.14)}")
print(f"square(2+3j) = {square(2+3j)}")  # Complex number!
print(f"square('ab') = {square('ab')}")  # String multiplication!

print("\n" + "=" * 60)
print("PART 4: Type Hints (Gradual Typing)")
print("=" * 60)

from typing import Protocol, List


class Quackable(Protocol):
    """
    Protocol: defines an interface without inheritance
    This is Python's way of making duck typing more explicit
    """

    def quack(self) -> str: ...


def make_it_quack_typed(thing: Quackable) -> str:
    """
    Type hints provide documentation and enable static checking
    But they're NOT enforced at runtime!
    """
    return thing.quack()


# These still work at runtime, even though we added type hints
print(f"Duck with type hint: {make_it_quack_typed(duck)}")
print(f"Person with type hint: {make_it_quack_typed(person)}")

# Type checkers (like mypy) can catch this error BEFORE running:
# make_it_quack_typed(dog)  # mypy would flag this!

print("\n" + "=" * 60)
print("PART 5: Comparison with OBJ Language")
print("=" * 60)

print(
    """
OBJ Language (from PLCC):
-------------------------
class Animal
    field name
    method speak = proc() "???"
end

class Dog extends Animal
    method speak = proc() "Woof!"
end

class Cat extends Animal
    method speak = proc() "Meow!"
end

define make_sound = proc(animal)
    .<animal>speak()

→ Requires inheritance hierarchy
→ Type checking via class membership


Python (Duck Typing):
--------------------
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:  # No inheritance needed!
    def speak(self):
        return "Beep boop"

def make_sound(thing):
    return thing.speak()

→ No inheritance required
→ Type checking via method existence (runtime)
→ More flexible, less safe


Python (with Protocols - Best of Both):
---------------------------------------
from typing import Protocol

class Speaker(Protocol):
    def speak(self) -> str: ...

def make_sound(thing: Speaker) -> str:
    return thing.speak()

→ No inheritance required (structural typing)
→ Type hints for static checking (optional)
→ Still duck typing at runtime
"""
)

print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)
print(
    """
1. Duck typing = structural typing at runtime
2. Static typing (PA7) = nominal typing at compile time
3. Python's approach: "We're all consenting adults here"
4. Protocols (PEP 544) bridge the gap
5. Type hints are optional and not enforced at runtime
"""
)
