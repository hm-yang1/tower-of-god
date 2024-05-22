from datetime import date
class Product:
    def __init__(self, name):
        self.name = name
        self.brand: str
        self.price: float
        self.release_date: date
        self.description = ''
        self.pros = []
        self.cons = []
        self.reviews = []
        self.score: int
    
    # Need to add function to fill in googable information, probably in scrapper
    
    def add_review(self, url: str):
        self.reviews.append(url)
    
    def add_pros(self, pro:str):
        self.pros.append(pro)
        
    def add_cons(self, con:str):
        self.cons.append(con)
    
    def add_description(self, des:str):
        if des.isspace(): return
        if self.description == '':
            self.description += des
        self.description = self.description + "\n" + des