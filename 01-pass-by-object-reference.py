"""
Pass-by-Object-Reference in Python
Demonstrates how Python's parameter passing differs from pass-by-value and pass-by-reference

Connection to PA6: Compare with call-by-value, call-by-reference, call-by-name, call-by-need
"""

print("=" * 60)
print("PART 1: Immutable Objects (act like pass-by-value)")
print("=" * 60)


def try_modify_int(x):
    """Attempt to modify an integer parameter"""
    print(f"  Inside function, before: x = {x}, id = {id(x)}")
    x = x + 10  # Creates NEW integer object
    print(f"  Inside function, after:  x = {x}, id = {id(x)}")
    return x


num = 5
print(f"Before call: num = {num}, id = {id(num)}")
result = try_modify_int(num)
print(f"After call:  num = {num}, id = {id(num)}")
print(f"Result:      result = {result}, id = {id(result)}")
print("\nObservation: Original num unchanged (immutable)")

print("\n" + "=" * 60)
print("PART 2: Mutable Objects (act like pass-by-reference)")
print("=" * 60)


def try_modify_list(lst):
    """Attempt to modify a list parameter"""
    print(f"  Inside function, before: lst = {lst}, id = {id(lst)}")
    lst.append(4)  # Modifies the SAME list object
    print(f"  Inside function, after:  lst = {lst}, id = {id(lst)}")


my_list = [1, 2, 3]
print(f"Before call: my_list = {my_list}, id = {id(my_list)}")
try_modify_list(my_list)
print(f"After call:  my_list = {my_list}, id = {id(my_list)}")
print("\nObservation: Original list WAS modified (mutable)")

print("\n" + "=" * 60)
print("PART 3: Reassignment vs. Mutation")
print("=" * 60)


def reassign_list(lst):
    """Reassigning the parameter creates a new binding"""
    print(f"  Inside, before reassignment: lst = {lst}, id = {id(lst)}")
    lst = [99, 98, 97]  # Creates NEW list, rebinds local name
    print(f"  Inside, after reassignment:  lst = {lst}, id = {id(lst)}")


def mutate_list(lst):
    """Mutating the object affects the original"""
    print(f"  Inside, before mutation: lst = {lst}, id = {id(lst)}")
    lst[:] = [99, 98, 97]  # Mutates the SAME object
    print(f"  Inside, after mutation:  lst = {lst}, id = {id(lst)}")


list1 = [1, 2, 3]
list2 = [1, 2, 3]

print("Testing reassignment:")
print(f"Before: list1 = {list1}, id = {id(list1)}")
reassign_list(list1)
print(f"After:  list1 = {list1}, id = {id(list1)}")
print("Result: Original unchanged (reassignment is local)")

print("\nTesting mutation:")
print(f"Before: list2 = {list2}, id = {id(list2)}")
mutate_list(list2)
print(f"After:  list2 = {list2}, id = {id(list2)}")
print("Result: Original changed (mutation affects object)")

print("\n" + "=" * 60)
print("PART 4: Custom Objects")
print("=" * 60)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


def move_point(p):
    """Mutate a point object"""
    p.x += 10
    p.y += 10


def replace_point(p):
    """Try to replace a point object"""
    p = Point(99, 99)  # Creates new object, rebinds local name
    return p


pt = Point(1, 2)
print(f"Original point: {pt}, id = {id(pt)}")

move_point(pt)
print(f"After move_point: {pt}, id = {id(pt)}")
print("Result: Point WAS mutated")

new_pt = replace_point(pt)
print(f"After replace_point: {pt}, id = {id(pt)}")
print(f"Returned new point: {new_pt}, id = {id(new_pt)}")
print("Result: Original unchanged, new object returned")

print("\n" + "=" * 60)
print("CONNECTION TO PA6 (Parameter Passing Mechanisms)")
print("=" * 60)
print(
    """
Call-by-value (PA6):        Pass a COPY of the value
                            → Python immutables BEHAVE like this

Call-by-reference (PA6):    Pass a REFERENCE to the original
                            → Python mutables BEHAVE like this

Pass-by-object-reference:   Pass a reference to the object
                            - Reassignment doesn't affect caller
                            - Mutation does affect caller
                            - Depends on object mutability

Key insight: Python ALWAYS passes object references,
but the effect depends on whether the object is mutable!
"""
)
