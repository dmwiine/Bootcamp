from app.room import Room
class Office(Room):
    def __init__(self,name):
        super().__init__(name)
        self.space_available = 6
        self.occupants = []


    def has_space(self):
        if self.space_available == 0:
            return False
        else:
            return True

    def add_person(self, person):
        person.office = self
        if self.space_available != 0:
            self.space_available -= 1
            self.occupants.append(person)
        return person

    def print_allocations(self):
        print(self.name)
        print("-----------------------------------------------------")
        print(",".join(occupant.name for occupant in self.occupants))