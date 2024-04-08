from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """
    p_start = R2Point
    p_end = R2Point

    @classmethod
    def set_line(cls, p_start, p_end):
        cls.p_start = p_start
        cls.p_end = p_end

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def cardinality(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p
        self._cardinality = 0
        if R2Point.deviation(Figure.p_start, Figure.p_end, self.p) == 0:
            self._cardinality = 1

    def add(self, q):
        if self.p == q:
            return self
        else:
            return Segment(self.p, q)

    def cardinality(self):
        return self._cardinality


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q
        if (R2Point.deviation(Figure.p_start, Figure.p_end, self.p)
                != R2Point.deviation(Figure.p_start, Figure.p_end, q)):
            self._cardinality = 1
        elif R2Point.deviation(Figure.p_start, Figure.p_end, self.p) == 0:
            self._cardinality = "continuum"
        else:
            self._cardinality = 0

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, r, self.q, self._cardinality)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)

    def cardinality(self):
        return self._cardinality


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, cardinality):
        self.points = Deq()
        self.points.push_first(b)
        self._cardinality = cardinality
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        if R2Point.deviation(Figure.p_start, Figure.p_end, b) == 0:
            if self._cardinality == 1:
                self._cardinality = "continuum"
            elif self._cardinality == 0:
                self._cardinality = 1
        elif (R2Point.deviation(Figure.p_start, Figure.p_end,
                                b) !=
              R2Point.deviation(Figure.p_start, Figure.p_end,
                                a)
              and (R2Point.deviation(Figure.p_start,
                                     Figure.p_end, b) !=
                   R2Point.deviation(Figure.p_start,
                                     Figure.p_end,
                                     c))
              and R2Point.deviation(Figure.p_start,
                                    Figure.p_end, c)
              + R2Point.deviation(Figure.p_start,
                                  Figure.p_end, a) != 0):
            self._cardinality = 2
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def cardinality(self):
        return self._cardinality

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # Пересчет множества пересечения
            if self._cardinality != 2:
                if R2Point.deviation(Figure.p_start, Figure.p_end, t) == 0:
                    if self._cardinality == 1:
                        self._cardinality = "continuum"
                    elif self._cardinality == 0:
                        self._cardinality = 1
                elif (R2Point.deviation(Figure.p_start, Figure.p_end,
                                        t) !=
                      R2Point.deviation(Figure.p_start, Figure.p_end,
                                        self.points.last())
                      and (R2Point.deviation(Figure.p_start,
                                             Figure.p_end, t) !=
                           R2Point.deviation(Figure.p_start,
                                             Figure.p_end,
                                             self.points.first()))
                      and ((R2Point.deviation(Figure.p_start,
                                              Figure.p_end,
                                              self.points.first())
                            + R2Point.deviation(Figure.p_start,
                                                Figure.p_end,
                                                self.points.last())
                            == 0) <= (self.points.size() > 2))):
                    self._cardinality = 2

            # добавление двух новых рёбер
            self._perimeter += (t.dist(self.points.first()) +
                                t.dist(self.points.last()))
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
