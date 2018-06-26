from datetime import date, time

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from creche.models import Child, JournalEntry


class ChildTest(TestCase):
    """Tests child model."""

    def test_create_child(self):
        """Check correct create child object."""
        Child.objects.create(name='Макс', gender=Child.GENDERS.BOY, birthdate=date(2018, 4, 13))

        self.assertEqual(Child.objects.all().count(), 1)


class JournalEntryTest(TestCase):
    """Tests journal."""

    def setUp(self):
        """Set up initial data."""
        self.child = Child.objects.create(name='Макс', gender=Child.GENDERS.BOY, birthdate=date(2018, 4, 13))

    def test_create_journal_entry(self):
        """Check correct create journal entry."""
        JournalEntry.objects.create(
            child=self.child,
            timestamp_come=time(12, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            datestamp=date(2018, 6, 26),
        )

        self.assertEqual(JournalEntry.objects.all().count(), 1)

    def test_create_journal_entry_with_away(self):
        """Check correct create journal entry with away data."""
        JournalEntry.objects.create(
            child=self.child,
            timestamp_come=time(12, 12, 12),
            timestamp_away=time(18, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            people_away=JournalEntry.PEOPLES.MOM,
            datestamp=date(2018, 6, 26),
        )

        self.assertEqual(JournalEntry.objects.all().count(), 1)

    def test_create_journal_entry_with_duplicate_child(self):
        """Check success when create duplicate child JournalEntry."""
        JournalEntry.objects.create(
            child=self.child,
            timestamp_come=time(12, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            datestamp=date(2018, 6, 26),
        )
        JournalEntry.objects.create(
            child=self.child,
            timestamp_come=time(12, 12, 12),
            timestamp_away=time(18, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            people_away=JournalEntry.PEOPLES.MOM,
            datestamp=date(2018, 6, 25),
        )

        self.assertEqual(JournalEntry.objects.all().count(), 2)

    def test_fail_create_journal_entry_with_duplicate_child_and_datestamp(self):
        """Check fail when create duplicate child and datetime JournalEntry."""
        JournalEntry.objects.create(
            child=self.child,
            timestamp_come=time(12, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            datestamp=date(2018, 6, 26),
        )
        with self.assertRaises(IntegrityError):
            JournalEntry.objects.create(
                child=self.child,
                timestamp_come=time(12, 12, 12),
                timestamp_away=time(18, 12, 12),
                people_come=JournalEntry.PEOPLES.DAD,
                people_away=JournalEntry.PEOPLES.MOM,
                datestamp=date(2018, 6, 26),
            )

    def test_fail_create_journal_entry_with_incomplete_away_data(self):
        """Check fail when create JournalEntry with incomplete away data."""
        entry_with_people_away = JournalEntry(
            child=self.child,
            timestamp_come=time(12, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            people_away=JournalEntry.PEOPLES.MOM,
            datestamp=date(2018, 6, 26),
        )
        entry_with_timestamp_away = JournalEntry(
            child=self.child,
            timestamp_come=time(12, 12, 12),
            timestamp_away=time(18, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            datestamp=date(2018, 6, 25),
        )
        with self.assertRaises(ValidationError):
            entry_with_people_away.full_clean()
        with self.assertRaises(ValidationError):
            entry_with_timestamp_away.full_clean()
