# Hash Map with Separate Chaining README

## Overview

`hash_map_sc.py` is an implementation of a hash map (hash table) using separate chaining as a collision resolution method. This script provides a basic yet efficient way to handle collisions by maintaining a linked list for each bucket within the hash table. When multiple keys hash to the same index, their values are stored in a linked list at that index, allowing multiple entries to exist in the same hash table space.

## Features

- **Separate Chaining Collision Handling:** Utilizes linked lists at each index of the hash table array to manage collisions efficiently.
- **Customizable Hash Function:** Offers flexibility to adapt or change the hash function according to specific needs or to improve distribution.
- **Key-Value Storage:** Enables storing and retrieving data in a key-value format, allowing quick access to values through keys.
- **Dynamic Resizing:** Though not implemented by default, the structure allows for future enhancements like dynamic resizing to maintain optimal load factors.

## Getting Started

### Prerequisites

- Python 3.x installed on your machine.

### Installation

No installation is necessary beyond ensuring Python is installed. Simply download `hash_map_sc.py` to your local environment.

### Running the Script

1. Open a terminal or command prompt.
2. Navigate to the directory containing `hash_map_sc.py`.
3. Run the script using Python:
   ```bash
   python hash_map_sc.py
   ```

## Usage

To use the hash map in your Python projects, import the `hash_map_sc.py` script and instantiate the `HashMap` class.

Example:
```python
from hash_map_sc import HashMap

# Create a new hash map instance
hash_map = HashMap()

# Insert key-value pairs
hash_map.put("key1", "value1")
hash_map.put("key2", "value2")

# Retrieve a value
value = hash_map.get("key1")
print(value)  # Output: value1

# Remove a key-value pair
hash_map.remove("key2")
```

## Customization

To customize the hash function or the linked list implementation, modify the `hash_map_sc.py` file. Ensure that any new hash function distributes keys uniformly to avoid potential performance issues.

## Contributing

Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more details.

Happy coding! 🚀
