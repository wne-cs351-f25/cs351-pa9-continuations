# CS351 - OBJ Keywords Deep Dive

**Date:** November 24, 2024
**Topic:** Understanding `self`, `super`, `myclass`, `!@`, and `superclass`

## Quick Reference

| Symbol       | Usage           | Purpose                                                                                                   | Context                    |
| ------------ | --------------- | --------------------------------------------------------------------------------------------------------- | -------------------------- |
| `self`       | `<self>x`       | Access members of the **original receiver** (the whole object). Enables dynamic dispatch (polymorphism).  | Instance Methods           |
| `this`       | `<this>x`       | Access members of the **current class instance**. Bypasses dynamic dispatch (ignores subclass overrides). | Instance Methods           |
| `super`      | `<super>x`      | Access members of the **parent class instance**. Used to call overridden methods from parent class.       | Instance Methods           |
| `myclass`    | `<myclass>x`    | Access **static members** (fields and procs) of the current class.                                        | Static & Instance Contexts |
| `superclass` | `<superclass>x` | Access **static members** of the parent class.                                                            | Static & Instance Contexts |
| `!@`         | `<!@>x`         | Access variables from the **lexical environment** where the class was defined (closure-like behavior).    | All Contexts               |

**Note:** `<self>` behaves like `this` in Java (dynamic). `<this>` in OBJ restricts access to the current class's implementation (similar to `super` but for the current class).

---

## Practice Problems

Predict the output of the following OBJ programs (check your answer with programs in OBJ/worksheet/).

### Problem 1: The "Three x's" (Static, Field, Parameter)

```obj
define A =
  class
    static x = 100
    field x

    method init = proc() {set x = 10; self}

    method calc = proc(x)
      % Which x is which?
      let
        param = x
        fld = <self>x
        stat = <myclass>x
      in
        +(+(param, fld), stat)
  end

define a = .<new A>init()
.<a>calc(1)
```

**Predicted Output:** \***\*\_\_\_\*\***

<details>
<summary>Reveal Solution</summary>

**Answer:** 111

- `x` (parameter) = 1
- `<self>x` (field) = 10
- `<myclass>x` (static) = 100
- 1 + 10 + 100 = 111
</details>

---

### Problem 2: Dynamic Dispatch with `self`

```obj
define Parent =
  class
    method identify = proc() 1

    method callWithSelf = proc() .<self>identify()
  end

define Child =
  class extends Parent
    method identify = proc() 2
  end

define c = new Child

{ display .<c>callWithSelf()  % What gets called?
; newline
}
```

**Predicted Output:** \***\*\_\_\_\*\***

<details>
<summary>Reveal Solution</summary>

**Answer:** 2

- `callWithSelf()` uses `<self>identify()`
- `self` refers to the original object `c` (an instance of `Child`)
- Dynamic dispatch finds `Child`'s overridden `identify` method
- Result: **2**

**Key Concept:** `self` enables polymorphism through dynamic dispatch

</details>

---

### Problem 3: The Lexical Window (`!@`)

```obj
define val = 10

define Container =
  class
    static val = 20
    field val

    method init = proc() {set val = 30; self}

    method getVals = proc()
      let
        lex = <!@>val     % Lexical environment where class was defined
        stat = <myclass>val  % Static field
      in
        +(lex, stat)
  end

define c = .<new Container>init()
define val = 999
.<c>getVals()
```

**Predicted Output:** \***\*\_\_\_\*\***

<details>
<summary>Reveal Solution</summary>

**Answer:** 1019

- `<!@>val`: Accesses the current value of `val` in the lexical environment (999)
- `<myclass>val`: Accesses the static field (20)
- Result: 999 + 20 = 1019

**Note:** In OBJ, `<!@>` provides access to the current lexical environment, capturing the most recent binding of `val` (which is 999 after the second define).

**Key Concept:** `<!@>` accesses the lexical environment, `<myclass>` accesses static fields

</details>

---

### Problem 4: Walking the Chain (`super` vs `superclass`)

```obj
define Top =
  class
    static id = 1
    method getID = proc() 10
  end

define Bottom =
  class extends Top
    static id = 2
    method getID = proc() 20

    method test = proc()
      let
        a = <superclass>id      % Access parent's static field
        b = .<super>getID()     % Call parent's instance method
      in
        +(a, b)
  end

define b = new Bottom
.<b>test()
```

**Predicted Output:** \***\*\_\_\_\*\***

<details>
<summary>Reveal Solution</summary>

**Answer:** 11

- `<superclass>id`: Accesses `Top`'s static field `id`. Value: **1**
- `.<super>getID()`: Calls `Top`'s instance method `getID`. Value: **10**
- Result: 1 + 10 = 11

**Key Concept:** `superclass` for static members, `super` for instance members of parent

</details>

---

### Problem 5: Static Context Access

```obj
define MyClass =
  class
    static x = 5
    static staticProc = proc()
      % Which of these are valid in static context?
      % A: <self>x - INVALID (no instance)
      % B: <myclass>x - VALID
      % C: <!@>x - VALID (if x exists in lexical scope)

      <myclass>x
    field x  % instance field (not accessible from static)
  end

.<MyClass>staticProc()
```

**Predicted Output:** \***\*\_\_\_\*\***

<details>
<summary>Reveal Solution</summary>

**Answer:** 5

- Static procedures (stored as static fields) have no instance context
- Cannot use `<self>` or `<super>` - would cause an error
- `<myclass>x` accesses the static field. Value: **5**

**Key Concept:** Static members can only access other static members or lexical scope

</details>

---

### Problem 6: Deep Inheritance Puzzle

```obj
define A =
  class
    method foo = proc() 1
    method test = proc() .<self>foo()
  end

define B =
  class extends A
    method foo = proc() 2
    method test = proc() .<super>test()
  end

define C =
  class extends B
    method foo = proc() 3
  end

define c = new C
.<c>test()
```

**Predicted Output:** \***\*\_\_\_\*\***

<details>
<summary>Reveal Solution</summary>

**Answer:** 3

- Call `.<c>test()` on instance of `C`
- `C` doesn't define `test`, so inherited from `B`
- `B.test` calls `.<super>test()` which calls `A.test`
- `A.test` calls `.<self>foo()`
- Crucially, `self` is **still** the original object `c` (instance of `C`)
- Dynamic dispatch looks for `foo` starting at `C`
- `C` implements `foo`, returning **3**

**Key Concept:** `self` preserves the original receiver through super calls

</details>

---

## Summary

Understanding OBJ's keyword system is crucial for the final exam:

1. **`self`** - Always refers to the original receiver (enables polymorphism)
2. **`this`** - Refers to the current class instance (bypasses dynamic dispatch)
3. **`super`** - Calls parent class methods (static dispatch to parent)
4. **`myclass`** - Access current class's static members
5. **`superclass`** - Access parent class's static members
6. **`<!@>`** - Access lexical environment where class was defined

Remember: OBJ uses `<self>` where Java/Python would use `this`/`self` for field access!
