class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
    def add_last(self, value):
        node = Node(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node
    def add_first(self, value):
        node = Node(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1
        return node
    def pop_first(self):
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        node.next = None
        self._size -= 1
        return node.value
    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next
    def find(self, pred):
        current = self.head
        while current:
            if pred(current.value):
                return current.value
            current = current.next
        return None
    def is_empty(self):
        return self._size == 0
    def size(self):
        return self._size
class Queue:
    def __init__(self):
        self._list = LinkedList()
    def enqueue(self, value):
        self._list.add_last(value)
    def dequeue(self):
        return self._list.pop_first()
    def __iter__(self):
        return iter(self._list)
    def is_empty(self):
        return self._list.is_empty()
class Stack:
    def __init__(self):
        self._list = LinkedList()
    def push(self, value):
        self._list.add_first(value)
    def pop(self):
        return self._list.pop_first()
    def is_empty(self):
        return self._list.is_empty()
    def __iter__(self):
        return iter(self._list)
