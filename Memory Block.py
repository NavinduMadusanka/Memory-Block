# Initialize the memory block parameters
class MemoryBlock :
    def __init__(self, start_address, size, processId=None) :
        self.start_address = start_address
        self.size = size
        self.processId = processId

    def is_free(self) :
        return self.processId is None


# initialize the operations of memory using first fit algorithm
class MemoryManager :
    def __init__(self, totalMemory, os) :
        self.total_memory = totalMemory
        self.os_files = os
        self.memory_map = []
        self.free_blocks = []

    def initialize_memory(self) :
        os_block = MemoryBlock(0, self.os_files)  # Create the os  block
        user_block = MemoryBlock(self.os_files, self.total_memory - self.os_files)  # Check for the rest of free blocks
        self.memory_map.append(os_block)  # Add os to memory block array
        self.memory_map.append(user_block)
        self.free_blocks.append(user_block)  # Add rest of the memory to free block array

    def allocate(self, processId, requested_size) :
        for block in self.free_blocks :  # Check for the free space (blocks)
            if block.size >= requested_size :  # Check the requested block is equal or lesser than the selected freeBlock
                if block.size == requested_size :  # If equal, then allocate and remove block from free block array
                    block.processId = processId
                    self.free_blocks.remove(block)
                else :
                    allocated_block = MemoryBlock(block.start_address, requested_size, processId)
                    # If lesser than selected block, then reduce from the free block, allocate the requested block
                    # and assign rest of the memory as a free block
                    free_block = MemoryBlock(block.start_address + requested_size, block.size - requested_size)
                    block.processId = processId
                    block.size = requested_size
                    self.free_blocks.remove(block)
                    self.free_blocks.append(free_block)
                    self.memory_map.append(free_block)
                return True
        return False

    def terminate(self, processId):  # Check the process id and terminate
        for block in self.memory_map:
            if block.processId == processId:
                block.processId = None
                self.free_blocks.append(block)  # Add the terminated block to free block array

    def print_memory_map(self) :
        print("Memory Map:")
        for block in self.memory_map :
            print(
                f"Block Start Address: {block.start_address} | Block Size: {block.size} | Process ID: {block.processId}")
        print()

    def print_free_blocks(self) :
        print("Free Blocks:")
        for block in self.free_blocks :
            print(f"Block Start Address: {block.start_address} | Block Size: {block.size}")
        print()


# Usage example
if __name__ == "__main__" :
    total_memory = 3560
    os_size = 400

    manager = MemoryManager(total_memory, os_size)
    manager.initialize_memory()

    # Allocate memory for processes
    manager.allocate("P1", 300)
    manager.allocate("P2", 600)
    manager.allocate("P3", 1000)
    manager.allocate("P4", 700)
    manager.allocate("P5", 400)
    print('******Before terminate*******')
    manager.print_memory_map()
    manager.print_free_blocks()

    # Deallocate memory for a process
    manager.terminate("P2")
    print('******After terminate*******')
    manager.print_memory_map()
    manager.print_free_blocks()
