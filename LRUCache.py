class LRUCache:

    def __init__(self, capacity: int):
        self.cache = dict()
        self.cache_capacity = capacity
        self.access_order = []
        

    def get(self, key: int) -> int:
        val = self.cache.get(key, -1)
        if val != -1:
            self.move_rightward(key)
        print(self.cache, '------g0',key, self.access_order)
        return val


    def put(self, key: int, value: int) -> None:
        if self.cache_capacity == 0:
            return
        if key in self.cache.keys():
            self.cache[key] = value
            self.move_rightward(key)
            print(self.cache, '------p1',key, self.access_order)
            return

        if len(self.cache) >= self.cache_capacity:
            least_recent = self.access_order[0]

            del self.cache[least_recent]
            self.access_order = self.access_order[1:]

            self.cache[key] = value
            self.access_order.append(key)
            print(self.cache, '------p2', self.access_order)
        else:
            self.cache[key] = value
            self.access_order.append(key)
            print(self.cache, '------P', self.access_order)

    def move_rightward(self, key: int) -> None:
        self.access_order.remove(key) 
        self.access_order.append(key) # Move to the rightmost end


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
