# Advent of Code 2022

A repo dedicated to my solutions of [AoC 2022](https://adventofcode.com/2022) - 
an annual advent calendar of small programming puzzles.

The solutions this year are mostly in Python and Kotlin, 
with the exception of [the first day](day_1.rock) that was my first attempt at
writing [Rockstar](https://codewithrockstar.com/)
Most of the solutions are "raw" (as-in my first take), but some of them have been refactored.


### Downloading input files

The python solutions don't have dependencies, but in order to download all inputs 
(and avoid keeping them in the repo), there is a small script in [`main.py`](main.py) that
utilizes [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data) to automate this.
To run it:
- first `pip install -r requirements.txt` (preferably in a venv) 
- and then run `python main.py`

### Requirements

Python requirements: **python 3.10+** (preferably PyPy, which results in 4-10x faster runtime of the implementations here)

Kotlin requirements: **Kotlin 1.4+** / **Java 8+**

Rockstar requirements: none, [developed online](https://codewithrockstar.com/), 
but will likely run just fine 
with a [local interpreter](https://github.com/RockstarLang/rockstar/tree/main/satriani) as well


