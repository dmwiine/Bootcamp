from app.office import Office
from app.living_space import LivingSpace
from app.staff import Staff
from app.fellow import Fellow


class Dojo():
    def __init__(self):
        self.all_offices= []
        self.all_living_spaces = []
        self.all_staff = []
        self.all_fellows = []

    def create_room(self, room_type, name_list):
        if room_type != "" and name_list != []:
            for name in name_list:
                if type(name) == str:
                    if room_type == "office":
                        office = Office(name)
                        self.all_offices.append(office)
                    elif room_type == "living_space":
                        living_space = LivingSpace(name)
                        self.all_living_spaces.append(living_space)
                    else:
                        raise TypeError
                else:
                    raise TypeError

        else:
            raise ValueError

    def add_fellow(self,name,wants_accomodation):
            fellow = Fellow(name)
            available_office = self.get_available_office()
            if available_office:
                fellow = available_office.add_person(fellow)
            if wants_accomodation == 'Y':
                fellow.wants_accomodation = True
                living_space = self.get_available_living_space()
                if living_space:
                    fellow = living_space.add_person(fellow)
            self.all_fellows.append(fellow)


    def add_staff(self,name):
            staff = Staff(name)
            available_office = self.get_available_office()
            if available_office:
                staff = available_office.add_person(staff)
            self.all_staff.append(staff)

    def get_available_office(self):
        for office in self.all_offices:
            if office.has_space():
                return office
        return False

    def get_available_living_space(self):
        for living_space in self.all_living_spaces:
            if living_space.has_space():
                return living_space

        return False
