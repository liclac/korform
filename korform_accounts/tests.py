from django.test import TestCase
from .models import Profile, User

class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='username', email='test@example.com', password='password',
            first_name=u"First", last_name=u"Last",
        )
    
    def test_profile_created(self):
        '''New users should have an associated profile.'''
        self.assertIsNotNone(self.user.profile)
    
    def test_profile_orphan_deleted(self):
        '''Orphaned profiles (no users) should be deleted.'''
        profile = self.user.profile
        self.user.delete()
        self.assertRaises(Profile.DoesNotExist, Profile.objects.get, pk=profile.pk)
    
    def test_profile_still_owned_remains(self):
        '''Profiles with users should not be deleted by one user being deleted.'''
        user2 = User.objects.create_user(username='user2', email='test2@example.com', profile=self.user.profile)
        self.assertEqual(self.user.profile, user2.profile)
        self.user.delete()
        Profile.objects.get(pk=user2.profile.pk)
    
    def test_shared_users_excludes_self(self):
        '''A member's shared users should not include itself.'''
        self.assertEqual([], list(self.user.get_shared_users()))
    
    def test_shared_users(self):
        '''Member's shared_users should work properly.'''
        user2 = User.objects.create_user(username='user2', email='test2@example.com', profile=self.user.profile)
        self.assertEqual([user2], list(self.user.get_shared_users()))
