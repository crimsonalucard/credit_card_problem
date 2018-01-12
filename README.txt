To run:
make sure you have python 3.6

run with
./main.py < input_file.txt
or
./main.py input_file.txt

to run tests
python3 -m unittest discover -s tests

type checking
mypy main.py
*mypy is experimental and still has some bugs. There is an error that it finds that I verified to be correct.

Design Decisions:

I wrote the program using a functional style while using type checking. This has the property of achieving haskell-
like correctness. Additionally by using functional programming I have ultimate granular modularity as each function
can only be a couple of lines long. This allows for better testing and easier future extension. Functions that do
IO operations are marked with the comment #IO and are generally not unit testable. A special case of IO are state functions
where I use impure functions to modify a global variable called state. For these stateful functions you cannot perform
unit tests but you can perform end to end tests and directly test the state of the global variable. Usually in functional
programming you can just have a function take in state and return a new state, however I decided to treat these state functions
as simulated IO in case the extension part of this assigment involves integrating the application with an external module
like redis or SQL.

Misc:

-Validation functions like checking if a charge is past the limit or Luhn10 are abstracted into decorators
So all charge, credits and other state changing functions are defined as a single arithmetic operation with
checking and other complicated things abstracted away into decorators. I often use this pattern for web views
so you'll literally see view functions that return raw data with all validation, json conversion and response object
packaging wrapped away in stacked decorators.

-Because the style is functional, there are no for loops anywhere within functional parts of the code. All looping
is done through reduce, list comprehensions (aka map/filter) or recursion. The exception is IO functions.
IO functions are impure anyway and retain the temporal aspects of imperative programming so I'll throw in for loops
into IO functions sometimes. In general, like haskell, I like to keep IO functions as small as possible so as to increase
the surface area of unit testable functions since IO functions cannot be unit tested. Also tests are informal so
I break a bunch of rules in the automated tests.

-mypy is an experimental type checker for python3 which supports type annotations. The python3 runtime itself does not
do any type checking.

-there are no external dependencies

