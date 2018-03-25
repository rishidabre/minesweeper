# minesweeper
Classic Minesweeper for playing on terminal.

## Overview
This is developed with Python 2.7.12 on Ubuntu 16.04 LTS. If you have a similar system, just download the script [minesweeper.py](minesweeper.py) and start by running:

`./minesweeper.py`

You will be prompted for configuration as follows:
```
Welcome to Minesweeper for terminal!
Configure the mines grid to begin (skip for default)...
Enter number of rows [16]: 5
Enter number of columns [16]: 6
Enter number of mines [40]: 7
```
Values enclosed in `[]` are default and you can hit enter to go with them.
The game now begins and the terminal will look like:
```
Let's begin...
Safe cells left:  23

0   1  2  3  4  5  6
1   -  -  -  -  -  -
2   -  -  -  -  -  -
3   -  -  -  -  -  -
4   -  -  -  -  -  -
5   -  -  -  -  -  -

Mark cell (col, row):
```
You can mark cells by passing in the row and column indices as a tuple (as shown).

Implementation details can be found as comments in the script.

## References
[1] https://en.wikipedia.org/wiki/Minesweeper_(video_game)
[2] http://minesweeperonline.com/#
