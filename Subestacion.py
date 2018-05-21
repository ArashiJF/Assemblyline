
class subestacion:
    def __init__(self,ultimo1,ultimo2,libre1, libre2):
        self.ultimo1 = ultimo1
        self.ultimo2 = ultimo2
        self.libre1 = libre1
        self.libre2 = libre2

    def get(self):
        return self.ultimo1,self.ultimo2,self.libre1,self.libre2