import json
from django.test import TestCase

from .models import User, Match, Message


class TestSum(TestCase):
    # Set up new user and login.
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='adminadmin',
            email='admin@example.com',
            level=3.0,
            gender='F',
            singles=True,
            doubles=True,
        )
        self.client.force_login(self.user)

    # Ensure models persist.
    def test_model_str(self):
        user = User.objects.create_user(
            username='user1',
            password='12345678',
            email='user1@user1.com',
            level=3.0,
            gender='F',
            singles=True,
            doubles=True,
        )
        self.assertEqual(User.objects.count(), 2)

        # Item model
        match = Match.objects.create(
            created_by=self.user,
            type='S'
        )
        match.match.add(user, self.user)
        match.save()
        self.assertEqual(Match.objects.count(), 1)
        saved_match = Match.objects.get(id=match.id)
        self.assertTrue(saved_match.new)

        message = Message.objects.create(
            text='This is a test message',
            match=match,
            created_by=self.user
        )
        self.assertEqual(Message.objects.count(), 1)

    def test_index_logged_in(self):
        User.objects.create_user(
            username='user1',
            password='12345678',
            email='user1@user1.com',
            level=3.0,
            gender='F',
            singles=True,
            doubles=True,
        )
        User.objects.create_user(
            username='user2',
            password='12345678',
            email='user2@user2.com',
            level=3.0,
            gender='F',
            singles=True,
            doubles=True,
        )
        User.objects.create_user(
            username='user3',
            password='12345678',
            email='user3@user3.com',
            level=3.0,
            gender='F',
            singles=True,
            doubles=True,
        )
        self.assertEqual(User.objects.count(), 4)
        response = self.client.post('/matches')
        content = json.loads(response.content)
        self.assertEqual(len(content['new_matches']), 4)
        doubles_new_match = [x for x in content['new_matches'] if x['type'] == 'D']
        self.assertEqual(len(doubles_new_match), 1)
        self.assertEqual(len(doubles_new_match[0]['match']), 4)
        single_new_matches = [x for x in content['new_matches'] if x['type'] == 'S']
        self.assertEqual(len(single_new_matches), 3)

    def test_index_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/')

    #   need to add check for html page

    def test_get_match(self):
        user = User.objects.create_user(
            username='user1',
            password='12345678',
            email='user1@user1.com',
            level=3.0,
            gender='F',
            singles=True,
            doubles=True,
        )

        match = Match.objects.create(
            created_by=self.user,
            type='S'
        )
        match.match.add(user, self.user)
        match.save()

        response = self.client.put('/match/' + str(match.id))
        content = json.loads(response.content)
        self.assertIsNotNone(content)

    def test_add_edit_message(self):
        user = User.objects.create_user(
            username='user1',
            password='12345678',
            email='user1@user1.com',
            level=3.0,
            gender='F',
            singles=True,
            doubles=True,
        )

        match = Match.objects.create(
            created_by=self.user,
            type='S'
        )
        match.match.add(user, self.user)
        match.save()

        response = self.client.post('/message/' + str(match.id),
                                    data=json.dumps(
                                        dict(text='This is a test post 2')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.filter(match=match).count(), 1)
        message = Message.objects.get(match=match)
        self.assertEqual(message.text, 'This is a test post 2')

        edit_response = self.client.post('/message/' + str(match.id),
                                         data=json.dumps(
                                             dict(id=message.id, text='This is a test post 2 - edited!')),
                                         content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.filter(match=match).count(), 1)
        edited_message = Message.objects.get(match=match)
        self.assertEqual(edited_message.text, 'This is a test post 2 - edited!')

    # def test_update_user(self):

