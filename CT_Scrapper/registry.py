
class RegistryArray:

    instance = None

    def __init__(self):
        self.items = []


    def getInstance(self):

        if self.instance == None:
            self.instance = RegistryArray()

        return self.instance


    def get_items(self):
        return self.items


    def append_item(self, item):
        self.items.append(item)
