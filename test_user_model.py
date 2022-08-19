"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follows, Likes

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

        self.u1 = User(
        email="test@test.com",
        username="testuser",
        password="HASHED_PASSWORD") #user ID 19

        self.u2 = User(
        email="test2@test.com",
        username="testuser2",
        password="HASHED_PASSWORD2" #user ID 20
        )

        self.client = app.test_client()

    def tearDown(self):
        """use rollback() to discard changes"""
        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""
        db.session.add(self.u1)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 0)

    
    def test_repr(self):
        """Does repr method work as expected"""

        db.session.add(self.u1)
        db.session.commit()

        self.assertEqual(self.u1.email, "test@test.com")
        self.assertEqual(self.u1.username, "testuser")


    
    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""

        db.session.add(self.u1)
        db.session.add(self.u2)
        db.session.commit()

        self.u1.following.append(self.u2)
        self.assertEqual(self.u1.following,[self.u2])


    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""
        db.session.add(self.u1)
        db.session.add(self.u2)
        db.session.commit()

        self.assertNotIn(self.u2,self.u1.following)

    
    def test_is_followed(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        db.session.add(self.u1)
        db.session.add(self.u2)
        db.session.commit()

        self.u1.followers.append(self.u2)
        self.assertEqual(self.u1.followers,[self.u2])


    def test_create_user(self):
        """Does User.create successfully create a new user given valid credentials?"""
        user = User.signup(
            username='created new user!',
            password='1212',
            email='thisis4testing@hotmail.com',
            image_url='https://media-cldnry.s-nbcnews.com/image/upload/newscms/2020_27/1586836/hotdogs-te-square-200702.jpg'
            )
        db.session.add(user)
        db.session.commit()
        self.assertIn(user,User.query.all())


    def test_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""
        user = User.signup(
            username='created new user!',
            password='1212',
            email='thisis4testing@hotmail.com',
            image_url='https://media-cldnry.s-nbcnews.com/image/upload/newscms/2020_27/1586836/hotdogs-te-square-200702.jpg'
            )
        db.session.add(user)
        db.session.commit()

        verify = User.authenticate('created new user!', '1212')

        self.assertEqual(user,verify)
        

    def test_failed_authenticate(self):
            """Does User.authenticate fail to return a user when given a valid username and password?"""
            user = User.signup(
                username='Beth',
                password='1212',
                email='thisis4testing@hotmail.com',
                image_url='https://media-cldnry.s-nbcnews.com/image/upload/newscms/2020_27/1586836/hotdogs-te-square-200702.jpg'
                )
            db.session.add(user)
            db.session.commit()

            verify = User.authenticate('Bella','2323')
            self.assertNotEqual(user,verify)