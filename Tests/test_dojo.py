import unittest
from app.dojo import Dojo

class TestDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_creates_office_successfully(self):

        initial_office_count = len(self.dojo.all_offices)
        self.dojo.create_room("office",["Blue"])
        #self.assertTrue(blue_office)
        new_office_count = len(self.dojo.all_offices)
        self.assertEqual(new_office_count - initial_office_count, len(["Blue"]))

    def test_creates_living_space_successfully(self):
        initial_living_space_count = len(self.dojo.all_living_spaces)
        self.dojo.create_room("living_space",["Blue"])
        #self.assertTrue(red_living_space)
        new_room_count = len(self.dojo.all_living_spaces)
        self.assertEqual(new_room_count - initial_living_space_count, 1)

    def test_add_fellow_successfully(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        fellow = self.dojo.add_fellow("Donna",'Y')
        self.assertTrue(fellow)
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

    def test_add_staff_successfully(self):
        initial_staff_count = len(self.dojo.all_staff)
        staff = self.dojo.add_staff("Donna")
        self.assertTrue(staff)
        new_staff_count = len(self.dojo.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1)

    def test_create_room_takes_only_string_parameters(self):
        self.assertRaises(TypeError,self.dojo.create_room, 1,[6])
        self.assertRaises(TypeError,self.dojo.create_room, 3.5,[0.87])

    def test_create_room_doesnt_take_empty__parameters(self):
        self.assertRaises(ValueError,self.dojo.create_room, "",[])
        self.assertRaises(ValueError,self.dojo.create_room, "Green",[])
        self.assertRaises(ValueError,self.dojo.create_room,"",["office"])

    def test_fellow_is_assigned_an_office_if_offices_available(self):
        self.dojo.create_room("office", ["Red"])
        fellow = self.dojo.add_fellow("Daph", 'Y')
        self.assertIsNotNone(fellow.office, msg="Fellow should be assigned an office")

    def test_staff_is_assigned_an_office_if_offices_are_available(self):
        self.dojo.create_room("office", ["Purple"])
        staff = self.dojo.add_staff("Daph")
        self.assertIsNotNone(staff.office, msg="Fellow should be assigned an office")

    def test_fellow_is_not_assigned_living_space_if_not_specified(self):
        self.dojo.create_room("living_space",["X","Y","Z"])
        fellow = self.dojo.add_fellow("Daph", 'N')
        self.assertIsNone(fellow.living_space, msg="Fellow should not be assigned living space if N")

    def test_fellow_is_assigned_living_space_if_specified(self):
        self.dojo.create_room("living_space",["A","B","C"])
        fellow = self.dojo.add_fellow("Daph", 'Y')
        self.assertIsNotNone(fellow.living_space, msg="Fellow should be assigned an office")

    def test_fellow_is_not_assigned_living_space_if_no_living_space_is_available(self):
        self.dojo.available_living_spaces = []
        fellow = self.dojo.add_fellow("Daph", 'Y')
        self.assertIsNone(fellow.living_space, msg="Fellow should not be assigned living space if no living space is available")

    def test_staff_is_not_assigned_office_if_no_office_is_available(self):
        self.dojo.available_offices = []
        staff = self.dojo.add_staff("Daph")
        self.assertIsNone(staff.office, msg="Staff should not be assigned office if no office is available")

    def test_fellow_is_not_assigned_office_if_no_office_is_available(self):
        self.dojo.available_offices = []
        fellow = self.dojo.add_fellow("Daph","Y")
        self.assertIsNone(fellow.office, msg="Fellow should not be assigned office if no office is available")

    def test_print_room_prints_all_the_names_as_expected(self):
        pass

        #def test_
        #def test_create_room_takes_list_parameter(self):
        #self.assertRaises(ValueError,self.dojo.create_room, "office","")


