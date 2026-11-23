"""Классы квадродерева и узла квадродерева"""

class QuadTreeNode:
    """
    Узел квадродерева - прямоугольная 
    область на плоскости, которая 
    содержит объекты
    """

    def __init__(self, bounds, capacity):
        self.bounds = bounds
        self.left, self.right, self.top, self.bottom  = bounds
        self.capacity = capacity

        self.objects = []
        self.children = [None, None, None, None]
        # 1 | 0
        # -----
        # 2 | 3

    def subdivide(self):
        """
        Создаёт детей узла и разделяет его 
        область на 4 подобласти
        """
        if not self.children[0]:

            suby = self.bottom + (self.top - self.bottom) / 2
            subx = self.left + (self.right - self.left) / 2

            child1 = QuadTreeNode((subx, self.right, self.top, suby), self.capacity)
            child2 = QuadTreeNode((self.left, subx, self.top, suby), self.capacity)
            child3 = QuadTreeNode((self.left, subx, suby, self.bottom), self.capacity)
            child4 = QuadTreeNode((subx, self.right, suby, self.bottom), self.capacity)

            self.children = [child1, child2, child3, child4]
        else:
            raise ValueError("У узла уже есть дети")


    @staticmethod
    def get_quadrant(obj, bounds):
        """
        Возвращает номер квадранта,
        в котором расположен объект
        """
        left, right, top, bottom = bounds
        if obj.x > left + (right - left) / 2:
            if obj.y > bottom + (top - bottom) / 2:
                return 0
            return 3
        if obj.y > bottom + (top - bottom) / 2:
            return 1
        return 2


    def insert(self, obj):
        """
        Помещает объект в узел. Если есть дети - рекурсивно 
        помещает в детей. Если объектов слишком много - 
        создаёт детей и распределяет объяекты по детям
        """

        if self.children[0]:
            quadrant = self.get_quadrant(obj, self.bounds)
            self.children[quadrant].insert(obj)
            return

        self.objects.append(obj)

        if len(self.objects) > self.capacity:
            self.subdivide()

            old_objects = self.objects
            self.objects = []

            for object in old_objects:
                self.insert(object)


    def remove(self, remove_obj):
        """
        Рекурсивно ищет объект в детях корня 
        и удаляет, если есть совпадение
        """

        for obj in self.objects:
            if obj == remove_obj:
                self.objects.remove(obj)
                return True

        if self.children[0]:
            quadrant = self.get_quadrant(remove_obj, self.bounds)
            child = self.children[quadrant]
            if child.remove(remove_obj):
                return True

        return False

    @staticmethod
    def intersects_circle(bounds, x, y, radius):
        """
        Проверка наличия пересечения 
        (или вхождения) квадранта и круглой области.
        Возвращает True, если пересечение есть.
        """
        left, right, top, bottom = bounds

        x_near = max(left, min(right, x))
        y_near = max(bottom, min(top, y))

        dist2 = (x - x_near)   ** 2 + (y - y_near) ** 2

        return dist2 <= radius ** 2


    def get_query(self, x, y, r, query_list=None):
        """
        Список объектов дерева, которые входят
        в круглую область. Рекурсивно ищем 
        пересечения области с квадрантами узла
        """

        if query_list is None:
            query_list = []

        if not self.intersects_circle(self.bounds, x, y, r):
            return query_list

        for obj in self.objects:
            if (obj.x - x) ** 2 + (obj.y - y) ** 2 <= r ** 2:
                query_list.append(obj)

        if self.children[0]:
            for child in self.children:
                child.get_query(x, y, r, query_list)

        return query_list


class QuadTree:
    """
    Квадродерево, в котором корень - вся 
    плоскость, а дети узла разбивают её на части
    """

    def __init__(self, bounds, capacity):
        self.bounds = bounds
        self.capacity = capacity

        self.root = QuadTreeNode(bounds, capacity)

    def insert(self, obj):
        """
        Рекурсивно проходится по детям корня
        и помещает объект в нужный квадрант
        """
        self.root.insert(obj)


    def remove(self, obj):
        """
        Рекурсивно ищет объект в детях корня 
        и удаляет, если есть совпадение
        """
        self.root.remove(obj)


    def get_query(self, x, y, r,):
        """
        Список объектов дерева, которые входят
        в круглую область. Рекурсивно ищем 
        пересечения области с квадрантами узла
        """
        return self.root.get_query(x, y, r)


    def clear(self):
        """Полностью очищает дерево"""

        self.root = QuadTreeNode(self.bounds, self.capacity)
