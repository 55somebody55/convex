#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void, Figure

Figure.set_line(R2Point(comment="Первая точка секущей прямой\n"),
                R2Point(comment="Вторая точка секущей прямой\n"))
f = Void()
try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, Мощность множества"
              f" пересечения - {f.cardinality()}")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
