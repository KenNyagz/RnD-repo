class LFUCache:

    def __init__(self, capacity: int):
        self.cache = dict()
        self.cache_capacity = capacity
        self.key_usage_count = {} #dict for storing cache usage count
        
    def get(self, key: int) -> int:
        val =  self.cache.get(key, -1)
        if val != -1:
            self.key_usage_count[key] += 1
        return val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.key_usage_count[key] += 1
            return

        if len(self.cache) > self.cache_capacity - 1:
            least_used_key = self.find_least_frequently_used_key()
            del(self.cache[least_used_key])
            del self.key_usage_count[least_used_key]
            self.cache[key] = value
            self.key_usage_count[key] = 1
            self.latest_added = key
        else:
            self.cache[key] = value
            self.key_usage_count[key] = 1  # Initialize key's count

    def reset_cache_count(self):
        for k in self.cache.keys():
            self.key_usage_count[k] = 0

    def find_least_frequently_used_key(self):
        least = 1000000 #Random high number
        key = ""  # Place holder for least key
        for key_, val in self.key_usage_count.items():
            if val < least:
                least = val
                key = key_
        return key

    def latest_added(self, key):
        latest_key = key
        
