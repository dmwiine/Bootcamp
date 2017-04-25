from app.room import Room
class Office(Room):
    def __init__(self,name):
        super().__init__(name)
        self.space_available = 6


    def has_space(self):
        if self.space_available == 0:
            return False
        else:
            return True

    def add_person(self, person):
        person.office = self
        if self.space_available != 0:
            self.space_available -= 1
        return person
