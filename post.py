class Post:
    def __init__(self, id, title, content, date):
        self.id = id
        self.title = title
        self.content = content
        self.date = date
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, id, title, content, date):
        new_post = Post(id, title, content, date)
        if not self.head:
            self.head = new_post
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_post

    def delete(self, id):
        current = self.head
        previous = None
        while current and current.id != id:
            previous = current
            current = current.next
        if not current:
            return False
        if not previous:
            self.head = current.next
        else:
            previous.next = current.next
        return True

    def update(self, id, new_title, new_content, new_date):
        current = self.head
        while current and current.id != id:
            current = current.next
        if not current:
            return False
        current.title = new_title
        current.content = new_content
        current.date = new_date
        return True

    def traverse(self):
        posts = []
        current = self.head
        while current:
            posts.append({
                'id': current.id, 
                'title': current.title, 
                'content': current.content,
                'date': current.date
            })
            current = current.next
        return posts