from django.test import TestCase

class TestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name="Test Product", description="test10285607", price=92187)

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