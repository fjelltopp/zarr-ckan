import pytest
from ckan.tests import factories
import ckan.model as model
from ckanext.zarr.plugin import ZaRRPlugin


@pytest.mark.ckan_config('ckan.plugins', "zarr")
@pytest.mark.usefixtures('clean_db', 'with_plugins')
class TestAuthentication:
    def test_successful_authentication_with_email(self):
        """Test successful authentication using email and correct password"""
        user = factories.User(
            email='test@example.com',
            password='correctpassword'
        )
        identity = {
            'login': 'test@example.com',
            'password': 'correctpassword'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)
        assert authenticated_user is not None
        assert authenticated_user.id == user['id']
        assert authenticated_user.is_active

    def test_case_insensitive_email(self):
        """Test that email authentication is case-insensitive"""
        user = factories.User(
            email='Test@Example.com',
            password='correctpassword'
        )
        # Try with lowercase email
        identity = {
            'login': 'test@example.com',
            'password': 'correctpassword'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)

        assert authenticated_user is not None
        assert authenticated_user.id == user['id']
        assert authenticated_user.is_active

    def test_wrong_password(self):
        """Test authentication fails with incorrect password"""
        factories.User(
            email='test@example.com',
            password='correctpassword'
        )
        identity = {
            'login': 'test@example.com',
            'password': 'wrongpassword'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)
        assert authenticated_user is None

    def test_wrong_password_with_different_case_email(self):
        """Test authentication fails with incorrect password and different case email"""
        factories.User(
            email='test@example.com',
            password='correctpassword'
        )
        identity = {
            'login': 'Test@Example.com',
            'password': 'wrongpassword'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)
        assert authenticated_user is None

    def test_nonexistent_user(self):
        """Test authentication fails for non-existent user"""
        identity = {
            'login': 'nonexistent@example.com',
            'password': 'anypassword'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)
        assert authenticated_user is None

    def test_inactive_user(self):
        """Test authentication fails for inactive user"""
        user = factories.User(
            email='test@example.com',
            password='correctpassword'
        )
        # Deactivate user
        user_obj = model.User.get(user['id'])
        user_obj.state = 'inactive'
        model.Session.commit()
        identity = {
            'login': 'test@example.com',
            'password': 'correctpassword'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)
        assert authenticated_user is None

    def test_empty_identity(self):
        """Test authentication fails with empty identity"""
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), None)
        assert authenticated_user is None

    def test_missing_password(self):
        """Test authentication fails with missing password"""
        factories.User(
            email='test@example.com',
            password='correctpassword'
        )
        identity = {
            'login': 'test@example.com'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)
        assert authenticated_user is None

    def test_missing_login(self):
        """Test authentication fails with missing login"""
        factories.User(
            email='test@example.com',
            password='correctpassword'
        )
        identity = {
            'password': 'correctpassword'
        }
        authenticated_user = ZaRRPlugin.authenticate(ZaRRPlugin(), identity)
        assert authenticated_user is None
