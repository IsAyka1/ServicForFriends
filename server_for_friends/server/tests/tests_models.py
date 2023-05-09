from django.test import TestCase
from ..models import User, Relation, FRIEND, REQUEST
# Create your tests here.


class UsersTestCase(TestCase):
    def setUpClass(self):

        user1 = User.objects.create(name='test1')
        user2 = User.objects.create(name='test2')
        user3 = User.objects.create(name='test3')

        Relation.objects.create(from_user=user1, to_user=user2, relation=FRIEND)
        Relation.objects.create(from_user=user1, to_user=user3, relation=REQUEST)
        Relation.objects.create(from_user=user3, to_user=user2, relation=REQUEST)

    def tearDownClass(cls):
        user1 = User.objects.get(name='test1')
        user2 = User.objects.get(name='test2')
        user3 = User.objects.get(name='test3')
        user1.delete()
        user2.delete()
        user3.delete()
        cls.assertEqual(User.objects.all().count(), 0)
        cls.assertEqual(Relation.objects.all().count(), 0)

    def test_users_count(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_arrivals_count(self):
        requests = Relation.objects.all()
        self.assertEqual(requests.count(), 3)

    def test_valid_relation(self):
        user1 = User.objects.get(name='test1')
        user2 = User.objects.get(name='test2')
        relation = Relation.objects.get(from_user=user1, to_user=user2)
        self.assertTrue(relation.is_valid_relation())
        self.assertEqual(relation.relation, FRIEND)

