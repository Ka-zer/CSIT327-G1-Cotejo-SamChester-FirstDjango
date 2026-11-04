from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class SignUpTests(TestCase):
    def test_signup_shows_success_message_and_cannot_set_role(self):
        response = self.client.post(reverse("signup"), {
            "username": "newbie", "email": "n@example.com",
            "first_name": "New", "last_name": "Bie", "course": "BSIT",
            "password1": "Str0ng-pass-123", "password2": "Str0ng-pass-123",
            "role": "ADMIN",  # must be ignored
        }, follow=True)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(any("created successfully" in str(m)
                            for m in get_messages(response.wsgi_request)))
        self.assertEqual(CustomUser.objects.get(username="newbie").role,
                         CustomUser.Role.STUDENT)

    def test_signup_redirects_authenticated_user(self):
        u = CustomUser.objects.create_user("a", password="x-Pass-12345")
        self.client.force_login(u)
        self.assertRedirects(self.client.get(reverse("signup")), reverse("dashboard"))


class ProfileTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            "stu", email="s@example.com", password="x-Pass-12345")
        self.other = CustomUser.objects.create_user("other", password="x-Pass-12345")

    def test_login_required(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_update_profile_with_success_message(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("profile"), {
            "first_name": "Stu", "last_name": "Dent",
            "email": "new@example.com", "course": "BSCS",
        }, follow=True)
        self.assertRedirects(response, reverse("profile"))
        self.assertContains(response, "updated successfully")
        self.user.refresh_from_db()
        self.assertEqual((self.user.first_name, self.user.course), ("Stu", "BSCS"))

    def test_cannot_escalate_role_or_edit_username(self):
        self.client.force_login(self.user)
        self.client.post(reverse("profile"), {
            "first_name": "S", "last_name": "T", "email": "s@example.com",
            "course": "", "role": "ADMIN", "username": "hacked",
            "is_superuser": "on", "is_staff": "on",
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, CustomUser.Role.STUDENT)
        self.assertEqual(self.user.username, "stu")
        self.assertFalse(self.user.is_superuser or self.user.is_staff)

    def test_edits_only_own_profile(self):
        self.client.force_login(self.user)
        self.client.post(reverse("profile"), {
            "first_name": "Mine", "last_name": "", "email": "", "course": ""})
        self.other.refresh_from_db()
        self.assertEqual(self.other.first_name, "")


class AccessTests(TestCase):
    def test_admin_panel_roles(self):
        student = CustomUser.objects.create_user("s", password="x-Pass-12345")
        admin = CustomUser.objects.create_user(
            "adm", password="x-Pass-12345", role=CustomUser.Role.ADMIN)
        url = reverse("admin_panel")
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(student)
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(admin)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_pages_load_bootstrap(self):
        for name in ("login", "signup"):
            self.assertContains(self.client.get(reverse(name)), "bootstrap@5")
