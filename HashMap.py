# Create Hash Map class

class HashMap:
    # empty initial buckets/capacity
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Citing: W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
    # inserts the new item into the hash table
    def insert(self, key, item):  # inserts & update
        # gets the bucket list where this item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if key not in bucket insert the item to the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # looks up items in the hash table
    def hash_lookup(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for pair in bucket_list:
            if key == pair[0]:
                return pair [1]
        return None

    # removes item from hash table
    def hash_remove(self, key):
        bucket = hash(key) % len(self.table)
        final = self.table[bucket]

        if key in final:
            final.remove(key)
