class Motorcycle:
    headings = ['ID', 'Brand', 'Model', 'Year', 'Price', 'Pos']
    fields = {
        '-ID-': 'Motorcycle ID:',
        '-Brand-': 'Brand:',
        '-Model-': 'Model:',
        '-Year-': 'Year:',
        '-Price-': 'Price:',
        '-PosFile-': 'Position into File'
    }

    def __init__(self, ID, brand, model, year, price, posFile):
        self.ID = ID
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.posFile = posFile
        self.erased = False

    def __eq__(self, other_motorcycle):
        return other_motorcycle.posFile == self.posFile

    def __str__(self):
        return (
            f"ID: {self.ID}, Brand: {self.brand}, Model: {self.model}, "
            f"Year: {self.year}, Price: {self.price}, Pos: {self.posFile}"
        )

    def motorcycleInPos(self, pos):
        return self.posFile == pos

    def setMotorcycle(self, brand, model, year, price,pos):
        # You may add validation checks here before updating the attributes
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.posFile = pos



