
# post.py
class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, title, content):
        new_post = Post(title, content)
        if not self.head:
            self.head = new_post
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_post

    def delete(self, title):
        current = self.head
        previous = None
        while current and current.title != title:
            previous = current
            current = current.next
        if not current:
            return False
        if not previous:
            self.head = current.next
        else:
            previous.next = current.next
        return True

    def update(self, old_title, new_title, new_content):
        current = self.head
        while current and current.title != old_title:
            current = current.next
        if not current:
            return False
        current.title = new_title
        current.content = new_content
        return True

    def traverse(self):
        posts = []
        current = self.head
        while current:
            posts.append({'title': current.title, 'content': current.content})
            current = current.next
        return posts
