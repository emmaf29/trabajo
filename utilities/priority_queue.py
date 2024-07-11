import heapq

class PriorityQueue:
    """
    Models a priority queue data structure, using a heap internally.
    """

    def __init__(self):
        self.__data = []
        self.__index = 0

    @property
    def is_empty(self):
        """ Answers if the queue is empty. """
        return len(self.__data) == 0

    @property
    def front(self):
        """
        Answers the element in the front of the queue,
        that is, the element with the highest priority,
        or None if the queue is empty.
        """
        return None if self.is_empty else self.__data[0][-1]

    def enqueue(self, item, priority):
        """ Add an element to the the queue using the given priority. """
        heapq.heappush(self.__data, (-priority, self.__index, item))
        self.__index += 1

    def dequeue(self):
        """ Remove the front element from queue and return it. """
        return heapq.heappop(self.__data)[-1]

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        return " <- ".join([str(e) for (p, i, e) in self.__data])
    
    def __iter__(self):
        return [e for (p, i, e) in sorted(self.__data)].__iter__()