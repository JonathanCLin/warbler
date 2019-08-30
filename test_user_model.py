"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()

        self.u1 = User.signup("uniqueusername1", "uniqueemail1@email.com", "PASSWORD", None)
        self.u2 = User.signup("uniqueusername2", "uniqueemail2@email.com", "PASSWORD", None)
        self.u3 = User.signup("uniqueusername3", "uniqueemail3@email.com", "PASSWORD", None)

        self.u1.id = 1
        self.u2.id = 2
        self.u3.id = 3
        db.session.add(self.u1)
        db.session.add(self.u2)
        db.session.add(self.u3)
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 0)
        self.assertEqual(repr(self.u1), "<User #1: uniqueusername1, uniqueemail1@email.com>")
        self.assertEqual(self.u1.is_following(self.u2), False)

    def test_is_following(self):

        self.u1.following.append(self.u2)

        self.assertEqual(self.u1.is_following(self.u2), True)
        self.assertEqual(self.u1.is_following(self.u2), 1)
        self.assertEqual(self.u1.is_following(self.u3), False)
        
    def test_is_followed_by(self):

        self.u1.following.append(self.u2)

        self.assertEqual(self.u2.is_followed_by(self.u1), True)
        self.assertEqual(self.u3.is_followed_by(self.u1), False)

    def test_usesr_create(self):

        u4 = User(id=4, email="test4@test.com", username="kim", password="password")
        db.session.add(u4)
        db.session.commit()

        user4 = User.query.get(4)

        u5 = User(id=5, email="test5@test.com", username="kim", password="password")

        self.assertEqual(user4.username, "kim")
        self.assertEqual(len(User.query.all()), 4)

    def test_user_authenticate(self):

        user = User.authenticate("uniqueusername1", "PASSWORD")
        user2 = User.authenticate("uniqueusername2", "PASSWORD2")
        user3 = User.authenticate("uniqusername2", "PASSWORD")
        

        self.assertEqual(user, self.u1)
        self.assertEqual(user2, False)
        self.assertEqual(user3, False)

