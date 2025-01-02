import time


class Block:
    def __init__(self, index, task_title, task_description, assignee, status, previous_hash=''):
        self.index = index
        self.task_title = task_title
        self.task_description = task_description
        self.assignee = assignee
        self.status = status
        self.timestamp = time.time()  # Timestamp for the block
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Simplified method to calculate the hash of a block.
        In practice, you'd use hashlib or another library for hashing.
        """
        block_string = f"{self.index}{self.task_title}{self.task_description}{self.assignee}{self.status}{self.timestamp}{self.previous_hash}"
        return str(hash(block_string))  # Simplified hash calculation

    def __str__(self):
        return f"Block(index={self.index}, task_title={self.task_title}, task_description={self.task_description}, assignee={self.assignee}, status={self.status}, timestamp={self.timestamp}, previous_hash={self.previous_hash})"


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block in the blockchain (Genesis block).
        """
        genesis_block = Block(index=0, task_title="Genesis Task", task_description="The first task", assignee="None",
                              status="Completed", previous_hash="0")
        self.chain.append(genesis_block)

    def add_task(self, task_title, task_description, assignee, status):
        """
        Add a new task to the blockchain.
        """
        index = len(self.chain)
        previous_block = self.chain[-1]
        previous_hash = previous_block.hash
        new_block = Block(index=index, task_title=task_title, task_description=task_description, assignee=assignee,
                          status=status, previous_hash=previous_hash)
        self.chain.append(new_block)

    def get_task(self, task_id):
        """
        Get task details by task ID.
        """
        if task_id < len(self.chain):
            return vars(self.chain[task_id])
        else:
            return None

    def update_task(self, task_id, task_data):
        """
        Update task details by task ID.
        """
        if task_id < len(self.chain):
            block = self.chain[task_id]
            block.task_title = task_data['task_title']
            block.task_description = task_data['task_description']
            block.assignee = task_data['task_assignee']
            block.status = task_data['task_status']
            block.hash = block.calculate_hash()
            return "Task updated successfully."
        else:
            return "Task not found."

    def delete_task(self, task_id):
        """
        Deletes a task (block) and reindexes the remaining blocks.
        """
        if task_id < 1 or task_id >= len(self.chain):
            return "Cannot delete the genesis block or a non-existent task."

        # Remove the task from the blockchain
        del self.chain[task_id]

        # Re-index subsequent blocks and recalculate their hashes
        for i in range(task_id, len(self.chain)):
            self.chain[i].index = i
            if i > 0:
                self.chain[i].previous_hash = self.chain[i - 1].hash
            self.chain[i].hash = self.chain[i].calculate_hash()

        return f"Task {task_id} deleted successfully."

    def get_all_tasks(self):
        """
        Get all tasks in the blockchain.
        """
        return [vars(block) for block in self.chain]
