# Python Knowledge Base

## Lists

A list is a mutable ordered collection in Python.

Lists can be modified after creation by adding, removing, or changing elements.

Example:

items = [1, 2, 3]
items[0] = 10

## Tuples

A tuple is an immutable ordered collection in Python.

Once created, its elements cannot be changed.

Example:

items = (1, 2, 3)

## Lists vs Tuples

The main difference is mutability.

Lists are mutable, while tuples are immutable.

Tuples can be useful when data should not be modified.

## Exception Handling

Python uses try, except, else, and finally blocks for exception handling.

try contains code that may raise an exception.

except handles specific exceptions.

else executes when no exception occurs.

finally executes regardless of whether an exception occurred.

Specific exception types should generally be handled instead of catching every exception with a broad except.