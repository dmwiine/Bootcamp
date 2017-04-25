from app.person import Person
class Fellow(Person):

    def __init__(self, name):
        super().__init__(name, None)
        self.living_space = None
        self.wants_accomodation = False