from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        Figure.set_line(R2Point(0, 0), R2Point(1, 1))
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)

    # Нульугольник не может быть пересечен прямой
    def test_cardinality(self):
        assert self.f.cardinality() == 0


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))
        self.g_line = R2Point(1, 0), R2Point(1, 1)
        self.f_line = R2Point(0, 0), R2Point(1, 1)
        Figure.set_line(self.g_line[0], self.g_line[1])

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    # Одноугольник может быть или пересечен, или не пересечен прямой
    def test_cardinality1(self):
        Figure.set_line(self.g_line[0], self.g_line[1])
        assert self.f.cardinality() == 0

    def test_cardinality2(self):
        Figure.set_line(self.f_line[0], self.f_line[1])
        self.f = Point(R2Point(0.0, 0.0))
        assert self.f.cardinality() == 1

    # При отсутствии изменений оболочки пересчет мощности не производится
    def test_cardinality0(self):
        Figure.set_line(self.g_line[0], self.g_line[1])
        self.f = Point(R2Point(0.0, 0.0))
        self.f.cardinality()
        assert self.f.add(R2Point(0.0, 0.0)).cardinality() == 0


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f_line = R2Point(0, 0), R2Point(1, 1)
        Figure.set_line(self.f_line[0], self.f_line[1])
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
        self.g_line = R2Point(0, 1), R2Point(2, 1)
        Figure.set_line(self.g_line[0], self.g_line[1])
        self.g = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
        self.h_line = R2Point(0, 0), R2Point(2, 0)
        Figure.set_line(self.h_line[0], self.h_line[1])
        self.h = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
        Figure.set_line(self.f_line[0], self.f_line[1])

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add4(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    # Двуугольник может быть пересечен или не пересечен прямой,
    # а также являться ее частью
    def test_cardinality1(self):
        assert self.f.cardinality() == 1

    def test_cardinality2(self):
        Figure.set_line(self.g_line[0], self.g_line[1])
        assert self.g.cardinality() == 0

    def test_cardinality3(self):
        Figure.set_line(self.h_line[0], self.h_line[1])
        assert self.h.cardinality() == "continuum"

    # При отсутствии изменений оболочки пересчет мощности не производится
    def test_cardinality0(self):
        self.g_line = R2Point(0, 1), R2Point(2, 1)
        self.g.cardinality()
        assert self.g.add(R2Point(0.0, 0.0)).cardinality() == 0


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        Figure.set_line(R2Point(0.0, 0.0), R2Point(1.0, 1.0))
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.g = Polygon(R2Point(0.0, 1.0),
                         R2Point(1.0, 2.0),
                         R2Point(0.0, 2.0), 0)
        self.h = Polygon(R2Point(0.0, -1.0),
                         R2Point(0.0, 0.0),
                         R2Point(1.0, 0.0), 0)
        self.s = Polygon(R2Point(0.0, -1.0),
                         R2Point(0.0, 0.0),
                         R2Point(1.0, 1.0), 1)
        self.f = Polygon(self.a, self.b, self.c, 2)

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon1(self):
        assert isinstance(self.f, Polygon)

    # Изменение порядка точек при создании объекта всё равно порождает Polygon
    def test_polygon2(self):
        self.f = Polygon(self.b, self.a, self.c, 1)
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3

    #   добавление точки внутрь многоугольника не меняет их количества
    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3

    #   добавление другой точки может изменить их количество
    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4

    #   изменения выпуклой оболочки могут и уменьшать их количество
    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))

    #   добавление точки может его изменить
    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_area1(self):
        assert self.f.area() == approx(0.5)

    #   добавление точки может увеличить площадь
    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    # Многоугольник может быть пересечен прямой в одной или двух точках,
    # или не пересечен прямой, также его граница может совпадать с прямой
    def test_cardinality010(self):
        assert self.g.cardinality() == 0

    def test_cardinality020(self):
        assert self.h.cardinality() == 1

    def test_cardinality030(self):
        assert self.f.cardinality() == 2

    def test_cardinality040(self):
        assert self.s.cardinality() == "continuum"

    def test_cardinality110(self):
        assert self.g.add(R2Point(1.0, 1.0)).cardinality() == 1

    def test_cardinality111(self):
        assert self.g.add(R2Point(1.0, 0.0)).cardinality() == 2

    def test_cardinality120(self):
        assert self.h.add(R2Point(1.6, 1.6)).cardinality() == "continuum"

    def test_cardinality121(self):
        assert self.h.add(R2Point(1.0, 4.0)).cardinality() == 2

    def test_cardinality140(self):
        assert self.s.add(R2Point(15.0, 73.0)).cardinality() == 2

    def test_cardinality310(self):
        assert (self.g.add(R2Point(1.0, 4.0))
                .add(R2Point(7.0, 8.0))
                .add(R2Point(-4.0, 0.0)).cardinality() == 0)

    def test_cardinality311(self):
        assert (self.g.add(R2Point(1.0, 4.0))
                .add(R2Point(1.0, 1.0))
                .add(R2Point(-4.0, 10.0)).cardinality() == 1)

    def test_cardinality312(self):
        assert (self.g.add(R2Point(4.0, 4.0))
                .add(R2Point(7.0, 8.0))
                .add(R2Point(-5.0, -5.0)).cardinality() == "continuum")

    def test_cardinality313(self):
        assert (self.g.add(R2Point(1.0, 4.0))
                .add(R2Point(7.0, 8.0))
                .add(R2Point(-4.0, -5.0)).cardinality() == 2)

    def test_cardinality320(self):
        assert (self.h.add(R2Point(-3.4, -6.8))
                .add(R2Point(-7.0, -10.0))
                .add(R2Point(1.0, 1.0)).cardinality() == "continuum")

    def test_cardinality000(self):
        Figure.set_line(R2Point(0.0, 0.0), R2Point(1.3, -1.3))
        self.s = Polygon(R2Point(0.0, -1.0),
                         R2Point(1.0, 1.0),
                         R2Point(0.0, 0.0), 1)
        assert self.s.cardinality() == 2

    def test_cardinality001(self):
        Figure.set_line(R2Point(0.0, 0.0), R2Point(1.0, -1.0))
        self.s = Polygon(R2Point(0.0, -1.0),
                         R2Point(1.0, 1.0),
                         R2Point(0.0, 0.0), 1)
        assert self.s.cardinality() == 2

    def test_cardinality002(self):
        Figure.set_line(R2Point(0.0, 0.0), R2Point(1.0, -1.0))
        self.s = Polygon(R2Point(0.0, -1.0),
                         R2Point(1.0, -3.0),
                         R2Point(0.0, 0.0), 1)
        assert self.s.cardinality() == 1

    def test_cardinality003(self):
        Figure.set_line(R2Point(3.0, 0.0), R2Point(1.0, -1.0))
        self.s = Polygon(R2Point(-5.0, -11.4),
                         R2Point(1.0, -3.0),
                         R2Point(-60.0, 987.9), 0)
        assert self.s.cardinality() == 0

    def test_cardinality_continuum_error(self):
        Figure.set_line(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
        self.s = Polygon(R2Point(0.0, 0.0),
                         R2Point(1.0, 1.0),
                         R2Point(1.0, 0.0), 'continuum')
        assert self.s.cardinality() == 'continuum'

    def test_cardinality_continuum_error2(self):
        Figure.set_line(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
        self.s = Polygon(R2Point(0.0, 0.0),
                         R2Point(-1.0, -1.0),
                         R2Point(1.0, 0.0), 'continuum')
        assert self.s.cardinality() == 'continuum'
