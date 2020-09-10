# Sudoku Solver
This solver uses an BFS algorithm, that recognize the best state of an arrangement of states, that continually increased and decreased by demand of the evolution of the tree.
# Initialization
The file init.py is the instance of the game, and accept input parameters about the initial assignment of any game.
```sh
python3.8 init.py
```
# Libraries
```sh
import copy
import pprint
import numpy as np
from queue import PriorityQueue
from random import shuffle
import gc
```
