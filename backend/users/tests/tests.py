from django.test import TestCase

class TestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("setUpClass")
    
    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
        super().tearDownClass()
    
    def setUp(self):
        print("setUp")
    
    def tearDown(self):
        print("tearDown")