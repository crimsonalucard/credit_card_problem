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
can only be a couple of lines long. This allows for better testing and easier future extensability. Functions that do
IO operations are marked with the comment #IO and are generally not unit testable. A special case of IO are state functions
where I use impure functions to modify a global variable called state. For these stateful functions you cannot perform
unit tests but you can perform end to end tests and directly test the state of the global variable. Usually in functional
programming you can just have a function take in state and return a new state, however I decided to treat these state functions
as simulated IO so in case the extension part of this assigment involves integrating "state" with an external module
like redis.

You will note that validation functions are split off into decorators for reuseability.