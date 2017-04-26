from app.office import Office
from app.living_space import LivingSpace
from app.staff import Staff
from app.fellow import Fellow
import random

class Dojo():
    def __init__(self):
        self.all_offices = []
        self.all_living_spaces = []
        self.all_staff = []
        self.all_fellows = []
        self.available_offices = []
        self.available_living_spaces = []

    def create_room(self, room_type, name_list):
        if room_type != "" and name_list != []:
            for name in name_list:
                if type(name) == str:
                    if room_type == "office":
                        office = Office(name)
                        self.all_offices.append(office)
                        self.available_offices.append(office)
                    elif room_type == "living_space":
                        living_space = LivingSpace(name)
                        self.all_living_spaces.append(living_space)
                        self.available_living_spaces.append(living_space)
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
                if fellow not in available_office.occupants and fellow.living_space is None:
                    fellow = available_office.add_person(fellow)
            if wants_accomodation == 'Y':
                fellow.wants_accomodation = True
                living_space = self.get_available_living_space()
                if living_space:
                    if fellow not in living_space.occupants and fellow.living_space is None:
                        fellow = living_space.add_person(fellow)
            self.all_fellows.append(fellow)
            self.update_available_offices()
            self.update_available_living_spaces()
            return fellow

    def add_staff(self,name):
            staff = Staff(name)
            available_office = self.get_available_office()
            if available_office:
                if staff not in available_office.occupants and staff.office is None:
                    staff = available_office.add_person(staff)
            self.all_staff.append(staff)
            self.update_available_offices()
            return staff

    def get_available_office(self):
        if len(self.available_offices) != 0:
            office = random.choice(self.available_offices)
            return office
        else:
            return False

    def get_available_living_space(self):
        if len(self.available_living_spaces) != 0:
            living_space = random.choice(self.available_living_spaces)
            return living_space
        else:
            return False

    def update_available_offices(self):
        for office in self.available_offices:
            if not office.has_space():
                self.available_offices.remove(office)
        return self.available_offices

    def update_available_living_spaces(self):
        for living_space in self.available_living_spaces:
            if not living_space.has_space():
                self.available_living_spaces.remove(living_space)
        return self.available_living_spaces

    def print_room(self,name):
        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            if room.name == name:
                for occupant in room.occupants:
                    print(occupant.name)

    def print_allocations(self):
        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            room.print_allocations()

    def print_unallocated(self):
        print("UnAllocated Fellows")
        for fellow in self.all_fellows:
            if fellow.living_space is None or fellow.office is None:
                print(fellow.name)
        print()
        print("UnAllocated Staff")
        for staff in self.all_staff:
            if staff.office is None:
                print(staff.name)

    def find_person(self, person_name):
        all_people = self.all_fellows + self.all_staff
        for person in all_people:
            if person.name == person_name:
                return person

    def find_room(self, room_name):
        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            if room.name == room_name:
                return room

    def reallocate_person(self,person_name,room_name):
        person = self.find_person(person_name)
        room = self.find_room(room_name)
        if room is LivingSpace:


