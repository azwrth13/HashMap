# Name: Christopher Reyes
# OSU Email: reyeschr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 3/14/23
# Description: HashMap implementation


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Inserts or updates a key-value pair in the hash map.
        """
        # Resize the table if the load factor exceeds or equals 1.0
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # Calculate the index for the key using the hash function
        index = self._hash_function(key) % self._capacity

        # Access the bucket at the calculated index
        bucket = self._buckets[index]

        # Attempt to find the node with the given key in the bucket's linked list
        node = bucket.contains(key)

        if node:
            # If the key is found, update the existing node's value
            node.value = value
        else:
            # If the key is not found, insert a new key-value pair into the bucket
            bucket.insert(key, value)
            # Increment the size of the hash map
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map to a new capacity, rehashing all existing key/value pairs.
        """
        # Ensure the new capacity is at least 1
        if new_capacity < 1:
            return

        # Adjust new_capacity to the next prime if it's not already prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Store the old buckets array and its capacity
        old_buckets = self._buckets
        old_capacity = self._capacity

        # Initialize a new array of buckets with the updated capacity
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(LinkedList())

        # Reset the hash map's size to 0; it will be updated as items are re-added
        self._size = 0
        self._capacity = new_capacity

        # Rehash all key/value pairs from the old buckets to the new buckets
        for i in range(old_capacity):
            bucket = old_buckets[i]
            if bucket:  # Check if the bucket is not empty
                current_node = bucket._head
                while current_node:
                    # Add each node's key/value pair to the new buckets
                    self.put(current_node.key, current_node.value)
                    current_node = current_node.next

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of the hash map.
        """
        # Calculate the load factor 
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Counts and returns the number of empty buckets in the hash map.
        """
        # Initialize a counter for empty buckets
        empty_count = 0  
        # Iterate through each bucket in the hash map
        for i in range(self._capacity):
            # Access each bucket using its index
            bucket = self._buckets[i]
            # Check if the current bucket is empty by seeing if its head node is None
            if bucket._head is None:
                # Increment the count for each empty bucket
                empty_count += 1  

        # Return the total number of empty buckets found
        return empty_count
    
    def get(self, key: str):
        """
        Retrieves the value associated with the given key from the hash map, if the key exists.
        """
        # Calculate the bucket index for the given key
        index = self._hash_function(key) % self._capacity

        # Access the bucket at the calculated index
        bucket = self._buckets[index]  # Check if the bucket is not empty

        if bucket is not None:
            # Search for the node with the specified key in the bucket's linked list
            node = bucket.contains(key)
            if node is not None:
                # If the node is found, return its value
                return node.value

        # If the key is not found, return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines if a given key is present in the hash map.
        """
        # Calculate the bucket index where the key would be located
        index = self._hash_function(key) % self._capacity
        # Access the appropriate bucket based on the index
        linked_list = self._buckets[index]

        # If the bucket is not empty, search for the key using the linked list's method
        if linked_list is not None:
            node = linked_list.contains(key)
            # Return True if the key is found, False otherwise
            return node is not None

        # If the bucket is empty, the key is not present in the hash map
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key and its associated value from the hash map if found.
        """
        # Calculate the bucket index for the given key
        index = self._hash_function(key) % self._capacity
        # Access the linked list at the calculated bucket index
        linked_list = self._buckets[index]

        # Check if the bucket is not empty and attempt to remove the key
        if linked_list is not None and linked_list.remove(key):
            # If the key is successfully removed, decrement the hash map's size
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Compiles and returns all key/value pairs in the hash map as a dynamic array of tuples.
        """
        # Initialize a new dynamic array to hold the key/value tuples
        result = DynamicArray()

        # Iterate through each bucket in the hash map
        for i in range(self._capacity):
            # Access the current bucket based on index
            bucket = self._buckets[i]
            # Check if the current bucket is not empty
            if bucket is not None:
                # Initialize traversal from the head of the linked list in the bucket
                node = bucket._head
                # Traverse through the linked list
                while node:
                    # Append the current node's key and value as a tuple to the result array
                    result.append((node.key, node.value))
                    # Move to the next node in the list
                    node = node.next

        # Return the dynamic array containing all key/value pairs
        return result

    def clear(self) -> None:
        """
        Resets the hash map to its initial empty state.
        """
        # Initialize the dynamic array for buckets
        self._buckets = DynamicArray()
        # Fill the dynamic array with empty linked lists for each bucket
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Reset the hash map's size to 0, indicating it's empty
        self._size = 0

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds and returns the modes in a dynamic array and their frequency.
    """
    # To count occurrences of each key
    key_map = HashMap() 
    # To track the highest frequency of any key
    max_freq = 0  

    # Count occurrences of each key and update max frequency
    for i in range(da.length()):
        current_key = da.get_at_index(i)
        if key_map.contains_key(current_key):
            current_freq = key_map.get(current_key) + 1
        else:
            current_freq = 1
        
        key_map.put(current_key, current_freq)
        max_freq = max(max_freq, current_freq)
    # To track which keys have been added to modes  
    mode_keys_added = HashMap()
    # To store mode keys
    modes = DynamicArray()  

    # Identify all keys with frequency equal to max_freq and collect them
    for i in range(da.length()):
        current_key = da.get_at_index(i)
        if key_map.get(current_key) == max_freq and not mode_keys_added.contains_key(current_key):
            modes.append(current_key)
            # Indicate this key has been added to modes
            mode_keys_added.put(current_key, None)  

    return modes, max_freq

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")