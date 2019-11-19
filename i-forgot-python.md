## Printing

print("yo!")

## Data Types

```python
mystring = "Holly's String"
myint = 10
myfloat = 20.0
myfloat = float(20)
```

You can cast something to a different data type with `int()`, `float()`, `str()`, etc.

## Globals

Variables declared outside of blocks statements and functions are global, however if you try to use them within a function you'll only get a copy that _cannot be modified_ (you'll get an error if you try).

To tell python to use the global version of the variable and allow you to modify it, use the `global` operator within the function:

```python
foo = 1

def add():
    global foo   # says give me a modifiable global, not a local copy
    foo = foo + 1

add()

print(foo) 	# result will be 2
```

## Arrays aka Collections

Python doesn't have arrays specifically, instead choose from the following data types:

**List**
	ordered, changeable, duplicates allowed, ["one", "two"]
**Tuple**
	ordered, unchangeable, duplicates allowed ("one", "two")
**Set**
	 unordered, unindexed, no duplicates {"one", "two"}
**Dictionary**
	unordered, changeable, indexed, no duplicates

Frequently used:

```python
my_empty_list = []
my_list = [1,2,3]    # can mix types, and nest lists.
my_list.append(4)
my_list[1] = 8		# list is now [1, 8, 3, 4]
print(my_list[0])    # returns 1
my_list.clear()		# list is now []
```

Other useful methods:

```python
my_collection.pop(1) # deletes the second element
my_collection.remove('this value') # removes the first occurrence
my_collection.copy() # returns a copy
my_collection.extend() # add the elements of a list (or anything iterable) to the end
my_collection.reverse() # reverses the order of the elements
my_collection.sort()
```

## Loops

```python
for item in my_collection:
	print(item)
```

`continue` sends you back to the top of the loop.

`break` will get you out of the loop completely.

```python
while x == True:
	print('still true!')
```

```python
while True:
	print('endless loop!')
```


## Conditionals

```python
if my_list[2] == 0:
	print('It is zero')
elif my_list[2] == 1:
	print('It is one')
else:
	print('It is not zero or one')
```

You can join expressions with `and`, `or`, and `not`.

## Functions aka Methods

A method is a function that belongs to a class/object.

```python
def name(parameters):
	# statements
```

## Processing Text

username, domain = message.split('@')

Concatenate strings with `+`:

```python
a = [1,2]
b = [3,4]
c = a + b
print(c) 	# returns [1,2,3,4]
```

Other useful methods:

```python
my_string.strip() 	# removes all whitespace in the string
my_string.upper()	# returns the string in all uppercase, does not modify it
```

## Math

The normal random module isn't in micropython, but here's a quick method to convert the random it does have into something more intuitive:

```python
def random(low,high):
    result = int(low + urandom.getrandbits(8) * (high - low) / 256)
    return result
```
