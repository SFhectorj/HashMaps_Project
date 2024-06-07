# Name: Hector Baeza
# OSU Email: baezah@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/6/2024
# Description: This assignment requires the implementation of a Hashmap class
# that uses a dynamic array to store the hash table, and implements Open Addressing
# with Quadratic Probing for collision resolution inside the dynamic array.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Parameter: Takes a string as a key and an object as a value.
        Adds a new key if the provided key is not present in the hashmap.
        If the key is already present then it updates its value.
        """
        # if the current load factor of the table is greater than or equal
        # to 0.5, the table must be resized to double its current capacity.
        if self.table_load() >= 0.5:    # need to implement table load
            self.resize_table(self._capacity * 2)

        # initial index needs to be calculated
        initial_index = self._hash_function(key) % self._capacity   # keeps the index within the hashtable
        index_count = 1     # Counter for the quadratic sequence

        # Search for an empty slot
        while True:
            active_entry = self._buckets[initial_index]
            if active_entry is None or active_entry.is_tombstone:
                self._buckets[initial_index] = HashEntry(key, value)
                self._size += 1
                return
            elif active_entry.key
            self._buckets[initial_index] is not None and not self._buckets[initial_index].is_tombstone:
            # Case 1: If the slot contains a key
            if self._buckets[initial_index].key == key:
                # Update with value & return
                self._buckets[initial_index].value = value
                return

            # Case 2: If the slot contains a different key
            # Use quadratic probing formula
            initial_index = (initial_index + index_count * index_count) % self._capacity
            index_count += 1

        # Insert the new key/value pair
        self._buckets[initial_index] = HashEntry(key, value)    # new hash entry object
        # reflects the new addition
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Parameter: Takes an integer as a new capacity
        This method changes the capacity of the table.
        The implementation rehashes the active key/value pairs into the new table.
        """
        # First check that new_capacity is not less than the current number of elements in the hash map
        if new_capacity < self._size:
            # if so, the method does nothing.
            return

        # If new_capacity is valid, make sure it is a prime number
        new_capacity = self._next_prime(new_capacity)

        # Create the new array
        new_buckets = DynamicArray()
        for i in range(new_capacity):
            # New buckets created and initialized to None
            new_buckets.append(None)

        # Rehash the key/value pairs
        old_buckets = self._buckets
        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0  # Reset

        # Proceed with rehashing using loop + put()
        for j in range(old_buckets.length()):
            active_entries = old_buckets[j]
            # Checks the entries are not empty or have a tombstone
            if active_entries is not None and not active_entries.is_tombstone:
                # Place in the correct position
                self.put(active_entries.key, active_entries.value)

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method is used to obtain the number of empty buckets in the hash table.
        """
        keeping_count = 0
        # Iterate over all buckets
        for i in range(self._buckets.length()):
            active_entries = self._buckets[i]
            # An empty bucket is either `None` or a tombstone.
            if active_entries is None or active_entries.is_tombstone:
                # count it
                keeping_count += 1

        return keeping_count

    def get(self, key: str) -> object:
        """
        Parameter: Takes a string as a 'key'
        This method will provide the associated value that comes with a key.
        """
        # Set variables
        hash_index = self._hash_function(key) % self._capacity  # hash function
        index_count = 0

        # Now implement quadratic probing
        while True:
            probed_index = (hash_index + index_count * index_count) % self._capacity
            active_entry = self._buckets[probed_index]

            # Check if the key is not in the hash map
            if active_entry is None:
                return None

            # The entry must not be a tombstone and match the provided key
            if not active_entry.is_tombstone and active_entry.key == key:
                # returns the value of the key
                return active_entry.value

            index_count += 1
            # Once the limit is reached, return none
            if index_count == self._capacity:
                return None

    def contains_key(self, key: str) -> bool:
        """
        Parameters: Takes a string as a key.
        This method checks if a given key exists in the hashmap.
        """
        # Set variables
        hash_index = self._hash_function(key) % self._capacity  # hash function
        index_count = 0

        # Now implement quadratic probing
        while True:
            probed_index = (hash_index + index_count * index_count) % self._capacity
            active_entry = self._buckets[probed_index]

            # Check if the key is not in the hash map
            if active_entry is None:
                return False

            # The entry must not be a tombstone and match the provided key
            if not active_entry.is_tombstone and active_entry.key == key:
                # confirms match
                return True

            index_count += 1
            # Once the limit is reached, return false
            if index_count == self._capacity:
                return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """
        # Set variables
        hash_index = self._hash_function(key) % self._capacity  # hash function
        index_count = 0

        # Now implement quadratic probing
        while True:
            probed_index = (hash_index + index_count * index_count) % self._capacity
            active_entry = self._buckets[probed_index]

            # Check if the key is not in the hash map
            if active_entry is None:
                return None

            # The entry must not be a tombstone and match the provided key
            if not active_entry.is_tombstone and active_entry.key == key:
                # Identify as a tombstone
                active_entry.is_tombstone = True
                # Factor out the tombstone
                self._size -= 1
                return

            index_count += 1
            # Once the limit is reached, return none
            if index_count == self._capacity:
                return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array with each index filled with a tuple of key/value pairs.
        """
        # begin with creating a new dynamic array
        da_output = DynamicArray()

        # Iterate through each bucket in the hash map
        for i in range(self._capacity):

            # Initialize the entry of each bucket
            active_entry = self._buckets[i]

            # The entry in the bucket must not be a tombstone and match the provided key
            if active_entry is not None and not active_entry.is_tombstone:
                # With conditions met, now the tuple can be added
                da_output.append((active_entry.key, active_entry.value))

        return da_output

    def clear(self) -> None:
        """
        This method simply clears the hashmaps by removing its contents.
        """
        # iterate the buckets of the hash table
        for i in range(self._capacity):
            # reset by setting to None
            self._buckets[i] = None

        # reset size with 0
        self._size = 0

    def __iter__(self):
        """
        Enables the hash map to iterate itself by returning the implemented HashMap Iterator class.
        """
        return HashMapIterator(self)


class HashMapIterator:
    def __init__(self, hash_map):
        # initializing the iterator
        self._hash_map = hash_map
        self._index = 0
        self._count = 0

    # Returns the instance itself
    def __iter__(self):
        return self

    def __next__(self):
        """
         Obtain next value and advance iterator
        """
        # iterate through the hashmap
        while self._index < self._hash_map.get_capacity():
            active_entry = self._hash_map._buckets[self._index]
            self._index += 1

            # The entry in the bucket must not be a tombstone and match the provided key
            if active_entry is not None and not active_entry.is_tombstone:
                self._count += 1

                return active_entry

        # The end of the hash map is reached
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
