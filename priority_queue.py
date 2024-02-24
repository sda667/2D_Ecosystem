import heapq
from typing import Generic, TypeVar


T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """
    Credits: Berkley AI Pacman Project
    """

    def __init__(self):
        self.heap: list[T] = []
        self.count = 0

    def push(self, item: T, priority: float):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self) -> T:
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def update(self, item: T, priority: float):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
