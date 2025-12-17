"""
Test dual conversion with manual calculation

Primal:
Min Z = x1 - x2 + 3x3
s.t.
x1 + x2 + x3 <= 10
2x1 - x3 <= 2
2x1 - 2x2 + 3x3 <= 62
x1, x2, x3 >= 0

Primal Solution: x1=0, x2=10, x3=0, Z*=-10

Standard Duality Theory (from Taha):
For Min with ≤ constraints, we use dual variables ≤ 0 (non-positive)
Or equivalently, substitute yi' = -yi where yi' ≥ 0

Dual (using y ≤ 0):
Max W = 10y1 + 2y2 + 62y3
s.t.
y1 + 2y2 + 2y3 ≤ 1
y1 - 2y3 ≤ -1
y1 - 2y2 + 3y3 ≤ 3
y1, y2, y3 ≤ 0

Substitute yi' = -yi (so yi = -yi', yi' ≥ 0):
Max W = -10y1' - 2y2' - 62y3'
s.t.
-y1' - 2y2' - 2y3' ≤ 1  => y1' + 2y2' + 2y3' ≥ -1
-y1' + 2y3' ≤ -1  => y1' - 2y3' ≥ 1
-y1' + 2y2' - 3y3' ≤ 3  => y1' - 2y2' + 3y3' ≥ -3
y1', y2', y3' ≥ 0

Let's solve manually:
From constraint 2: y1' ≥ 1 + 2y3'
To maximize W = -10y1' - 2y2' - 62y3', we want to minimize y1', y2', y3'

Set y3' = 0, y2' = 0:
From constraint 2: y1' ≥ 1
Try y1' = 1:
- Constraint 1: 1 ≥ -1 ✓
- Constraint 2: 1 ≥ 1 ✓
- Constraint 3: 1 ≥ -3 ✓

W* = -10(1) - 2(0) - 62(0) = -10 ✓ Matches!

So the dual solution is y1=1, y2=0, y3=0 (in terms of y')
"""

print(__doc__)
