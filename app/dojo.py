from app.office import Office
from app.living_space import LivingSpace
from app.staff import Staff
from app.fellow import Fellow
import random
import _sqlite3
import datetime
from Models.models import engine
from sqlalchemy.orm import sessionmaker
from Models.models import Office
from Models.models import Fellow
from Models.models import Staff
from Models.models import LivingSpace

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

    def add_fellow(self, name, wants_accomodation):
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

    def print_room(self, name):
        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            if room.name == name:
                for occupant in room.occupants:
                    print(occupant.name)

    def print_allocations(self):
        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            room.print_allocations()

    def print_allocations_to_a_file(self):
        all_rooms = self.all_offices + self.all_living_spaces
        file = open('./Files/allocations.txt', 'w')
        for room in all_rooms:
            if not len(room.occupants) != 0:
                file.write('\n' + room.name + '\n')
                file.write("-----------------------------------------------------"'\n')
                file.write(",".join(occupant.name for occupant in room.occupants).upper() + '\n')

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

    def print_unallocated_to_file(self):
        file = file = open('./Files/unallocated.txt', 'w')
        file.write('\n'"UnAllocated Fellows"'\n')
        for fellow in self.all_fellows:
            if fellow.living_space is None or fellow.office is None:
                file.write(fellow.name + '\n')
        file.write('\n')
        file.write('\n'"UnAllocated Staff"'\n')
        for staff in self.all_staff:
            if staff.office is None:
                file.write(staff.name + '\n')


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

    def reallocate_person(self, person_name, room_name):
        person = self.find_person(person_name)
        room = self.find_room(room_name)

        if room is LivingSpace and room in self.available_living_spaces:
            person.living_space.occupants.remove(person)
            person.living_space.space_available += 1
            room.add_person(person)

        elif room is Office and room in self.available_offices:
            person.office.occupants.remove(person)
            person.office.space_available += 1
            room.add_person(person)
        else:
            return "Room selected has no available space"

    def load_people(self, file_name):
        file = open(file_name,'r')
        wants_accomodation = "N"

        for line in file.readlines():
            inputs = line.split()
            name = inputs[0] + " " + inputs[1]
            person_type = inputs[2]

            if len(inputs) == 4:
                wants_accomodation = inputs[3]
            if person_type == "FELLOW":
                self.add_fellow(name,wants_accomodation)
            elif person_type == "STAFF":
                self.add_staff(name)

    def save_state(self):
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Create objects
        for living_space in self.all_living_spaces:
            session.add(living_space)

        for office in self.all_offices:
            session.add(office)

        for fellow in self.all_fellows:
            session.add(fellow)

        for staff in self.all_staff:
            session.add(staff)

        # commit the record the database
        session.commit()

    def load_state(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        # Create objects
        for living_space in session.query(LivingSpace).order_by(LivingSpace.living_space_id):
            self.all_living_spaces.append(living_space)

        for office in session.query(Office).order_by(Office.office_id):
            self.all_offices.append(office)

        for fellow in session.query(Fellow).order_by(Fellow.fellow_id):
            self.all_fellows.append(fellow)

        for staff in session.query(Staff).order_by(Staff.staff_id):
            self.all_staff.append(staff)

