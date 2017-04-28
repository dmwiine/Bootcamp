from app.office import Office
from app.living_space import LivingSpace
from app.staff import Staff
from app.fellow import Fellow
from Models.models import engine
from sqlalchemy.orm import sessionmaker
from Models.models import OfficeModel
from Models.models import FellowModel
from Models.models import StaffModel
from Models.models import LivingSpaceModel

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
        # This function creates new rooms which are either offices or living spaces

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
        # Function to add a fellow and allocate him/her a room

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
        # Function to add a staff and allocate him/her a room

            staff = Staff(name)
            available_office = self.get_available_office()
            if available_office:
                if staff not in available_office.occupants and staff.office is None:
                    staff = available_office.add_person(staff)
            self.all_staff.append(staff)
            self.update_available_offices()
            return staff


    def get_available_living_space(self):
        # This function randomizes the living_space selection

        if len(self.available_living_spaces) != 0:
            living_space = random.choice(self.available_living_spaces)
            return living_space
        else:
            return False

    def get_available_office(self):
        # This function randomizes the office selection

        if len(self.available_offices) != 0:
            office = random.choice(self.available_offices)
            return office
        else:
            return False

    def update_available_offices(self):
        # Function to check and update available offices

        for office in self.available_offices:
            if not office.has_space():
                self.available_offices.remove(office)
        return self.available_offices

    def update_available_living_spaces(self):
        # Function to check and update available living_spaces

        for living_space in self.available_living_spaces:
            if not living_space.has_space():
                self.available_living_spaces.remove(living_space)
        return self.available_living_spaces

    def print_room(self, name):
        # This function prints the occupants in a room

        all_rooms = self.all_offices + self.all_living_spaces
        print("**** Room " + name + " occupants ****")
        print()
        for room in all_rooms:
            if room.name == name:
                for occupant in room.occupants:
                    print(occupant.name)

    def print_allocations(self):
        # Print rooms and their corresponding allocations

        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            room.print_allocations()

    def print_allocations_to_a_file(self, filename):
        # Prints room allocations to a text file

        all_rooms = self.all_offices + self.all_living_spaces
        file = open('./Files/' + filename, 'w')
        for room in all_rooms:
            if len(room.occupants) > 0:
                file.write('\n' + room.name + '\n')
                file.write("-----------------------------------------------------"'\n')
                file.write(",".join(occupant.name for occupant in room.occupants).upper() + '\n')

    def print_unallocated(self):
        # Prints all the people who haven't been allocated rooms

        print("**** UnAllocated Fellows ****")
        for fellow in self.all_fellows:
            if fellow.living_space is None or fellow.office is None:
                print(fellow.name)
            else:
                print("None found")
        print()
        print("**** UnAllocated Staff ****")
        for staff in self.all_staff:
            if staff.office is None:
                print(staff.name)
            else:
                print("None found")

    def print_unallocated_to_file(self,filename):
        # Prints all the people who haven't been allocated rooms to a text file

        file = file = open('./Files/' + filename, 'w')
        file.write('\n'"**** UnAllocated Fellows ****"'\n')
        for fellow in self.all_fellows:
            if fellow.living_space is None or fellow.office is None:
                file.write(fellow.name + '\n')
        file.write('\n')
        file.write('\n'"**** UnAllocated Staff ****"'\n')
        for staff in self.all_staff:
            if staff.office is None:
                file.write(staff.name + '\n')


    def find_person(self, person_name):
        # Function to find a person object given their name

        all_people = self.all_fellows + self.all_staff
        for person in all_people:
            if person.name == person_name:
                return person

    def find_room(self, room_name):
        # Function to find a room object given room name

        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            if room.name == room_name:
                return room

    def reallocate_person(self, person_name, room_name):
        # Function to reallocate a person to a new room

        person = self.find_person(person_name)
        room = self.find_room(room_name)

        if room is LivingSpace and room in self.available_living_spaces:
            person.living_space.occupants.remove(person)
            person.living_space.space_available += 1
            room.add_person(person)
            room.occupants.append(person)
        elif room is Office and room in self.available_offices:
            person.office.occupants.remove(person)
            person.office.space_available += 1
            room.add_person(person)
            room.occupants.append(person)
        else:
            return "Room selected has no available space"

    def load_people(self, file_name):
        # Function to load people from a text file

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
        # Function to save session data into the database

        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Create objects
        for living_space in self.all_living_spaces:
            living_space_model = LivingSpaceModel(living_space.name, living_space.space_available)
            session.add(living_space_model)

        for office in self.all_offices:
            office_model = OfficeModel(office.name, office.space_available)
            session.add(office_model)

        for fellow in self.all_fellows:
            with session.no_autoflush:
                living_space = None
                office = None
                office_query = None
                space_query = None
                if fellow.living_space:
                    space_query = session.query(LivingSpaceModel).filter_by(
                        name=fellow.living_space.name).first()
                if fellow.office:
                    office_query = session.query(OfficeModel).filter_by(name=fellow.office.name).first()
                if space_query:
                    living_space = space_query.living_space_id
                if office_query:
                    office = office_query.office_id
                fellow_model = FellowModel(fellow.name, living_space, office)
                session.add(fellow_model)

        for staff in self.all_staff:
            with session.no_autoflush:
                office = None
                office_query = None
                if staff.office:
                    office_query = session.query(OfficeModel).filter_by(name=staff.office.name).first()
                if office_query:
                    office = office_query.office_id

                staff_model = StaffModel(office, staff.name)
                session.add(staff_model)

        # commit the record the database
        session.commit()

    def load_state(self):
        # Function to load data from the database

        Session = sessionmaker(bind=engine)
        session = Session()

        # Create objects
        for living_space in session.query(LivingSpaceModel).order_by(LivingSpaceModel.living_space_id):
            new_space = LivingSpace(living_space.name)
            new_space.space_available = living_space.spaces_available
            self.all_living_spaces.append(new_space)

        for office in session.query(OfficeModel).order_by(OfficeModel.office_id):
            new_office = Office(office.name)
            new_office.space_available = office.spaces_available
            self.all_offices.append(new_office)

        for fellow in session.query(FellowModel).order_by(FellowModel.fellow_id):
            new_fellow = Fellow(fellow.name)
            if fellow.living_space:
                fellow_space = LivingSpace(fellow.living_space.name)
                fellow_space.space_available = fellow.living_space.spaces_available
                new_fellow.living_space = fellow_space

            if fellow.office:
                office = Office(fellow.office.name)
                office.space_available = fellow.office.spaces_available
                new_fellow.office = office

            self.all_fellows.append(new_fellow)

        for staff in session.query(StaffModel).order_by(StaffModel.staff_id):
            new_staff = Staff(staff.name)
            if staff.office:
                office = Office(staff.office.name)
                office.space_available = staff.office.spaces_available
                new_staff.office = office
            self.all_staff.append(new_staff)

