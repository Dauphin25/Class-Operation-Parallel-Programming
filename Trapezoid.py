
import random as rd
import time
import threading
from multiprocessing import Pool

class Trapezoid:
    def __init__(self, sides=None):
        if sides is None:
            sides = [0, 0, 0]
        self.a = min(sides)
        self.b = max(sides)
        self.h = sum(sides) - self.a - self.b

    def area(self):
        return int(((self.a + self.b) / 2) * self.h)

    def __str__(self):
        return ('ტოლფერდა ტრაპეციის დიდი ფუძეა -> {},'
                ' პატარა ფუძეა -> {},'
                ' ხოლო სიმაღლეა ->{}').format(self.b, self.a, self.h)

#  Implements the equality operator (==).
    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()
        return False
#  Implements the not equal operator (!=).
    def __ne__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__eq__(other)
        return False
#  Implements the less than operator (<).
    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False
# Implements the greater than operator (>).
    def __gt__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False
#  Implements the addition operator (+).
    def __add__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() + other.area()
        print("Error massage: passed parameter isn't Trapezoid")
#  Implements the subtraction operator (-).
    def __sub__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() - other.area()
        print("Error massage: passed parameter isn't Trapezoid")
#  Implements the multiplication operator (*).
    def __mul__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() * other.area()
        print("Error massage: passed parameter isn't Trapezoid")
# Implements the floor division operator (//).
    def __floordiv__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() // other.area()
        print("Error massage: passed parameter isn't Trapezoid")
# Implements the modulo operator (%).
    def __mod__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() % other.area()
        print("Error massage: passed parameter isn't Trapezoid")


class Rectangle(Trapezoid):
    def __init__(self, sides=None):
        if sides is None:
            sides = [0, 0]
        super().__init__([sides[0], sides[0], sides[1]])

    def __str__(self):
        return ("მართკუთხედის სიმაღლეა -> {}, "
                "ხოლო სიგანე -> {}").format(self.a, self.b)

    def area(self):
        return int(self.a * self.b)


class Square(Trapezoid):
    def __init__(self, side=None):
        if side is None:
            side = [0]
        super().__init__([side[0], side[0], side[0]])

    def __str__(self):
        return "კვადრატის გვერდია -> {}".format(self.a)


def calculate_trapezoid_area(trapezoids, start, end):
    start = int(start)
    end = int(end)
    for i in range(start, end):
        Trapezoid(trapezoids[i]).area()

def calculate_rectangle_area(rects, start, end):
    start = int(start)
    end = int(end)
    for i in range(start, end):
        Rectangle(rects[i]).area()

def calculate_square_area(my_squars, start, end):
    start = int(start)
    end = int(end)
    for i in range(start, end):
        Square(my_squars[i]).area()

def calculate_with_regular_way(trapezoids, rects, my_squares):
    start = time.perf_counter()

    for trapezoid in trapezoids:
        Trapezoid(trapezoid).area()

    for rectangle in rects:
        Rectangle(rectangle).area()

    for square in my_squares:
        Square(square).area()

    finish = time.perf_counter()

    print("time to compute areas of my figures in a ~~regular way~~ is: ", round(finish - start, 2), 'second(s)')

def calculate_with_threads(trapezoids, rects, my_squares, num_of_figures):
    start1 = time.perf_counter()
    counter = 0
    threads = []
    for i in range(10):
        t1 = threading.Thread(target=calculate_trapezoid_area, args=(trapezoids, counter, counter + num_of_figures/10))
        t2 = threading.Thread(target=calculate_rectangle_area, args=(rects, counter, counter + num_of_figures / 10))
        t3 = threading.Thread(target=calculate_square_area, args=(my_squares, counter, counter + num_of_figures / 10))
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        counter =+ num_of_figures/10

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


    finish1 = time.perf_counter()

    print("time to compute areas of my figures using  *Threads* is: ", round(finish1 - start1, 2), 'second(s)')

def calculate_with_threads_for_processes(trapezoids, rects, my_squares, num_of_figures):

    counter = 0
    threads = []
    for i in range(10):
        t1 = threading.Thread(target=calculate_trapezoid_area, args=(trapezoids, counter, counter + num_of_figures/10))
        t2 = threading.Thread(target=calculate_rectangle_area, args=(rects, counter, counter + num_of_figures / 10))
        t3 = threading.Thread(target=calculate_square_area, args=(my_squares, counter, counter + num_of_figures / 10))
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        counter =+ num_of_figures/10

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def calculate_with_pools(trapezoids, rects, my_squares, num_of_figures):
    start2 = time.perf_counter()
    with Pool(processes=10) as pool:
        # Map the functions to the respective lists and collect the results
        trapezoid_areas = pool.starmap(calculate_trapezoid_area, [(trapezoids, i, i + num_of_figures // 10) for i in
                                                                  range(0, num_of_figures, num_of_figures // 10)])
        rectangle_areas = pool.starmap(calculate_rectangle_area, [(rects, i, i + num_of_figures // 10) for i in
                                                                  range(0, num_of_figures, num_of_figures // 10)])
        square_areas = pool.starmap(calculate_square_area, [(my_squares, i, i + num_of_figures // 10) for i in
                                                            range(0, num_of_figures, num_of_figures // 10)])

    finish2 = time.perf_counter()

    print("time to compute areas of my figures using ->Pools<- is: ", round(finish2 - start2, 2), 'second(s)')



if __name__ == "__main__":

    number_of_figures = 10000

    trapecoids = [[rd.randint(1, 200), rd.randint(
        1, 200), rd.randint(1, 200)] for _ in range(number_of_figures)]

    rectangles = [[rd.randint(1, 200), rd.randint(1, 200)] for _ in range(number_of_figures)]

    squares = [[rd.randint(1, 200)] for _ in range(number_of_figures)]
# time to compute areas of my figures using ^^processes with threads^^ is:  0.36 second(s)
    start3 = time.perf_counter()
    processes = []
    for i in range(5):
        process = threading.Thread(target=calculate_with_threads_for_processes, args=( trapecoids, rectangles, squares, number_of_figures))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    finish3 = time.perf_counter()
    print("time to compute areas of my figures using ^^processes with threads^^ is: ", round(finish3 - start3, 2), 'second(s)')

# time to compute areas of my figures in a ~~regular way~~ is:  0.02 second(s)
    calculate_with_regular_way(trapecoids, rectangles, squares)
# time to compute areas of my figures using  *Threads* is:  0.05 second(s)
    calculate_with_threads(trapecoids, rectangles, squares, number_of_figures)
# time to compute areas of my figures using ->Pools<- is:  0.34 second(s)
    calculate_with_pools(squares, rectangles, squares, number_of_figures)