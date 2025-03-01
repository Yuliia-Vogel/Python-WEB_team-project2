from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Contact
from .forms import ContactForm
from datetime import date, timedelta

User = get_user_model()


# -------------------- Model Tests -------------------- #
class ContactModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_create_contact(self):
        contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            phone="1234567890",
            email="john.doe@example.com",
            birthday="1990-01-01",
            user=self.user,
        )
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(contact.user, self.user)

    def test_contact_str_method(self):
        contact = Contact.objects.create(
            first_name="John", last_name="Doe", user=self.user
        )
        self.assertEqual(str(contact), "John Doe")

    def test_contact_without_email(self):
        contact = Contact.objects.create(
            first_name="Jane", last_name="Doe", phone="0987654321", user=self.user
        )
        self.assertIsNone(contact.email)

    def test_contact_birthday(self):
        contact = Contact.objects.create(
            first_name="Alice",
            last_name="Smith",
            phone="1234567890",
            birthday=date(1985, 5, 15),
            user=self.user,
        )
        self.assertEqual(contact.birthday, date(1985, 5, 15))

    def test_contact_creation_without_required_fields(self):
        contact = Contact(first_name="", last_name="", email="")
        with self.assertRaises(ValidationError):
            contact.full_clean()


# -------------------- Form Tests -------------------- #
class ContactFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "phone": "+1234567890",
            "email": "john.doe@example.com",
            "birthday": "1990-01-01",
        }

    def test_valid_form(self):
        form = ContactForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        invalid_data = self.valid_data.copy()
        invalid_data["phone"] = "12345"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_invalid_phone_number_with_non_digit(self):
        invalid_data = self.valid_data.copy()
        invalid_data["phone"] = "12345ABC"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_phone_number_with_invalid_length(self):
        invalid_data = self.valid_data.copy()
        invalid_data["phone"] = "+1234"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_required_field_first_name(self):
        invalid_data = self.valid_data.copy()
        invalid_data["first_name"] = ""
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_missing_required_field_last_name(self):
        invalid_data = self.valid_data.copy()
        invalid_data["last_name"] = ""
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_birthday_field_format(self):
        invalid_data = self.valid_data.copy()
        invalid_data["birthday"] = "01-01-1990"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("birthday", form.errors)


# -------------------- Views Tests -------------------- #
class ContactViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        self.contact1 = Contact.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1234567890",
            address="123 Main St",
            birthday=date(1990, 2, 14),
        )
        self.contact2 = Contact.objects.create(
            user=self.user,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone="+1987654321",
            address="456 Elm St",
            birthday="1985-02-02",
        )

    def test_contact_list_view(self):
        url = reverse("contacts:contact-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact1.first_name)
        self.assertContains(response, self.contact2.first_name)

    def test_contact_detail_view(self):
        url = reverse("contacts:contact-detail", kwargs={"pk": self.contact1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact1.first_name)
        self.assertContains(response, self.contact1.last_name)

    def test_contact_create_view(self):
        url = reverse("contacts:contact-create")
        data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "phone": "+1555555555",
            "address": "789 Oak St",
            "birthday": "1992-03-03",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(first_name="Alice").exists())

    def test_contact_update_view(self):
        url = reverse("contacts:contact-update", kwargs={"pk": self.contact1.pk})
        data = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "phone": "+1234567890",
            "address": "123 Main St",
            "birthday": "1990-01-01",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.last_name, "Smith")

    def test_contact_delete_view(self):
        url = reverse("contacts:contact-delete", kwargs={"pk": self.contact1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(pk=self.contact1.pk).exists())

    def test_contact_list_with_search_query(self):
        url = reverse("contacts:contact-list")
        response = self.client.get(url, {"query": "John"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact1.first_name)
        self.assertNotContains(response, self.contact2.first_name)

    def test_contact_list_with_birthday_filter(self):
        today = date.today()
        birthday = today + timedelta(days=20)

        self.contact1 = Contact.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            birthday=birthday,
        )

        response = self.client.get(reverse("contacts:contact-list"), {"days_ahead": 30})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact1.first_name)

    def test_contact_list_no_birthday_filter(self):
        url = reverse("contacts:contact-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact1.first_name)
        self.assertContains(response, self.contact2.first_name)

    def test_contact_list_birthday_filter_with_invalid_value(self):
        url = reverse("contacts:contact-list")
        response = self.client.get(url, {"days_ahead": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact1.first_name)
        self.assertContains(response, self.contact2.first_name)

