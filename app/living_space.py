from app.room import Room
class LivingSpace(Room):
    def __init__(self,name):
        super().__init__(name)
        self.space_available = 4



        def has_space(self):
            if self.space_available == 0:
                return False
            else:
                return True

        def add_person(self,fellow):
            fellow.living_space = self
            if self.space_available != 0:
                self.space_available -= 1
            return fellow
