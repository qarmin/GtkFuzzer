# GtkFuzzer
Simple GTK Fuzzer which aims to test all available classes and functions in GTK


## How it should work
1. Loop, execute steps below x times
2. Get list of all classes
3. Throw out classes which crashes when instancing etc.(this should be reported before to bug tracer)
4. Create object with for each class
5. Get list of all methods of this classes
6. Throw out all methods which cause bugs - e.g. which crashes or just shouldn't be used like object.free()
7. Throw out all methods which arguments are not supported
8. Execute every function with random or not parameters
9. Clean object before executing next method on object(this is optional, clearing object will allow to have reproducible results)


## Current status
For now only most of classes are created and none of function is executed

## How to use it
- Install Python3
- Install GTK 3(can be probably easily changed to GTK4 if needed)
- Install required PyGobject dependences - https://pygobject.readthedocs.io/en/latest/getting_started.html#ubuntu-getting-started
- Run `python3 main.py`