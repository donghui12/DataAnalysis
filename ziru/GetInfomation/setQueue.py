from queue import Queue
"""
    建立一个无重复的Queue队列
"""


class SetQueue(Queue):
    def _init(self, maxsize):
        self.all_items = set()
        Queue._init(self, maxsize)

    def put(self, item, block=True, timeout=None):
        if item not in self.all_items:
            self.all_items.add(item)
            Queue.put(self, item, block, timeout)

