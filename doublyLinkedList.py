class NodeDLL:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
        
# Empty Doubly Linked List
class DoublyLinkedList:
    def __init__(self):
        self.head = None
 
    # Inserts a new node on the front of list
    
    def add(self, new_data): 
        if self.head is None:
            self.head = new_data
            self.tail = new_data
        else:
            self.tail.next = new_data
            new_data.prev = self.tail
            self.tail = new_data
 
    def printList(self):
        if(self.head is None):
            print('Empty!')
        else:
            node = self.head
            while(node is not None):
                print(node.data, end = ' '),
                node = node.next 
            
    def remove(self, current_node):
        successor_node = current_node.next
        predecessor_node = current_node.prev

        if successor_node is not None:
            successor_node.prev = predecessor_node

        if predecessor_node is not None:
            predecessor_node.next = successor_node

        if current_node is self.head:
            self.head = successor_node

        if current_node is self.tail:
            self.tail = predecessor_node
            
    def insert_after(self, current_node, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        elif current_node is self.tail:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        else:
            successor_node = current_node.next
            new_node.next = successor_node
            new_node.prev = current_node
            current_node.next = new_node
            successor_node.prev = new_node
            
    def prepend(self, new_node):
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node