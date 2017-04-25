import unittest
from app.dojo import Dojo

class TestDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_creates_office_successfully(self):

        initial_office_count = len(self.dojo.all_offices)
        blue_office = self.dojo.create_room("office",["Yellow","Black"])
        #self.assertTrue(blue_office)
        new_office_count = len(self.dojo.all_offices)
        self.assertEqual(new_office_count - initial_office_count, len(["Yellow","Black"]))
    def test_creates_living_space_successfully(self):
        initial_living_space_count = len(self.dojo.all_living_spaces)
        red_living_space = self.dojo.create_room("living_space",["Blue"])
        #self.assertTrue(red_living_space)
        new_room_count = len(self.dojo.all_living_spaces)
        self.assertEqual(new_room_count - initial_living_space_count, 1)

    def test_add_fellow_successfully(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        fellow = self.dojo.add_fellow("Donna",True)
        #self.assertTrue(fellow)
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

    def test_add_staff_successfully(self):
        initial_staff_count = len(self.dojo.all_staff)
        staff = self.dojo.add_staff("Donna")
        #self.assertTrue(staff)
        new_staff_count = len(self.dojo.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1)

    def test_create_room_takes_only_string_parameters(self):
        self.assertRaises(TypeError,self.dojo.create_room, 1,[6])
        self.assertRaises(TypeError,self.dojo.create_room, 3.5,[0.87])

    def test_create_room_doesnt_take_empty__parameters(self):
        self.assertRaises(ValueError,self.dojo.create_room, "",[])
        self.assertRaises(ValueError,self.dojo.create_room, "Green",[])
        self.assertRaises(ValueError,self.dojo.create_room,"",["office"])

        #def test_create_room_takes_list_parameter(self):
        #self.assertRaises(ValueError,self.dojo.create_room, "office","")




