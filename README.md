# lego-gear-calculator

gear_calculator.py accepts a gear ratio as the input and prints a list of gear
trains that can be used to achieve that ratio. It can use a worm gear, 8, 12,
16, 20, 24, 36, 40, or 56 tooth gears.

Example:

```
dwalton@laptop ~/l/lego-gear-calculator> ./gear_calculator.py 27 4

Ratio: 27:4

Solutions
=========
Gear Train: 12:8 36:8
Gear Train: 24:8 36:16
Gear Train: 36:8 36:24
Gear Train: 36:12 36:16

dwalton@laptop ~/l/lego-gear-calculator>
```
