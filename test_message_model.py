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


class MessageModelTestCase(TestCase):
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

        m1 = Message("i like treats", 1)
        self.m2 = Message("i like turtles")
        self.m3 = Message("i don't like kim")

        self.u1.id = 1
        self.u2.id = 2
        self.u3.id = 3
        db.session.add(self.m1)
        db.session.add(self.m2)
        db.session.add(self.m3)
        db.session.commit()

    def test_message_belongs_to_user(self):

        self.assertEqual(self.u1.messages[0], self.m1)
