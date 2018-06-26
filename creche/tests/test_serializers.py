from datetime import date, time

from django.test import TestCase

from creche.models import Child, JournalEntry
from creche.serializers import (
    ChildSerializer,
    JournalEntryCreateSerializer,
    JournalEntryListSerializer,
    JournalEntryUpdateSerializer,
)


class ChildSerializerTest(TestCase):
    """Tests child serializer."""

    def test_create_child(self):
        """Test correct create childs."""
        child = ChildSerializer(data={'name': 'Luisa', 'gender': 'girl', 'birthdate': '2000-12-28'})
        self.assertEqual(child.is_valid(), True)
        child.save()

        self.assertEqual(Child.objects.all().count(), 1)


class JourneyListSerializerTest(TestCase):
    """Tests JourneyEntry List serializer."""

    def setUp(self):
        """Setup initial data."""
        child = Child.objects.create(name='Макс', gender=Child.GENDERS.BOY, birthdate=date(2018, 4, 13))
        pupil = Child.objects.create(
            name='Лана',
            gender=Child.GENDERS.GIRL,
            birthdate=date(2008, 4, 13),
            is_pupil=True,
            classroom=4,
        )

        JournalEntry.objects.create(
            child=child,
            timestamp_come=time(12, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            datestamp=date(2018, 6, 26),
        )
        JournalEntry.objects.create(
            child=pupil,
            timestamp_come=time(12, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            datestamp=date(2018, 6, 26),
        )

    def test_correct_queryset(self):
        """Check correct queryset (all)."""
        serializer = JournalEntryListSerializer(JournalEntry.objects.all(), many=True)
        self.assertEqual(len(serializer.data), 2)

    def test_correct_fields_count(self):
        """Check correct queryset (all)."""
        serializer = JournalEntryListSerializer(JournalEntry.objects.first())
        self.assertEqual(len(serializer.data), 7)
        self.assertEqual(
            sorted(serializer.data.keys()),
            ['child', 'datestamp', 'id', 'people_away', 'people_come', 'timestamp_away', 'timestamp_come'],
        )


class JourneyCreateSerializerTest(TestCase):
    """Tests JourneyEntry Create serializer."""

    def setUp(self):
        """Setup initial data."""
        self.child = Child.objects.create(name='Макс', gender=Child.GENDERS.BOY, birthdate=date(2018, 4, 13))
        self.serializer_class = JournalEntryCreateSerializer

    def test_correct_create(self):
        """Check correct create."""
        entry = self.serializer_class(data={'child': self.child.id, 'people_come': JournalEntry.PEOPLES.DAD})
        self.assertEqual(entry.is_valid(), True)
        entry.save()

        self.assertEqual(JournalEntry.objects.all().count(), 1)

    def test_dont_save_datestamp_in_create(self):
        """Check when create entry with correct datestamp."""
        datestamp = date(2016, 5, 26)

        entry = self.serializer_class(data={
            'child': self.child.id,
            'people_come': JournalEntry.PEOPLES.DAD,
            'datestamp': datestamp.strftime('%Y-%m-%d'),
        })
        self.assertEqual(entry.is_valid(), True)
        # with self.assertRaises(AttributeError):
        entry_object = entry.save()
        self.assertNotEqual(entry_object.datestamp, datestamp)

    def test_not_valid_duplicate_create(self):
        """Check serializer fail after errors in unique."""
        entry = self.serializer_class(data={'child': self.child.id, 'people_come': JournalEntry.PEOPLES.DAD})
        self.assertEqual(entry.is_valid(), True)
        entry.save()
        entry_not_valid = self.serializer_class(data={'child': self.child.id, 'people_come': JournalEntry.PEOPLES.DAD})
        self.assertEqual(entry_not_valid.is_valid(), False)
        self.assertEqual(entry_not_valid.errors['non_field_errors'][0].code, 'unique')


class JourneyUpdateSerializerTest(TestCase):
    """Tests JourneyEntry Update serializer."""

    def setUp(self):
        """Set Up initial data."""
        child = Child.objects.create(name='Макс', gender=Child.GENDERS.BOY, birthdate=date(2018, 4, 13))

        self.journal_entry = JournalEntry.objects.create(
            child=child,
            timestamp_come=time(12, 12, 12),
            people_come=JournalEntry.PEOPLES.DAD,
            datestamp=date(2018, 6, 26),
        )
        self.serializer_class = JournalEntryUpdateSerializer

    def test_correct_update(self):
        """Check correct update."""
        entry = self.serializer_class(self.journal_entry, data={'people_away': JournalEntry.PEOPLES.DAD})
        self.assertEqual(entry.is_valid(), True)
        entry.save()

        self.assertEqual(JournalEntry.objects.all().count(), 1)
        self.assertEqual(JournalEntry.objects.first().people_away, JournalEntry.PEOPLES.DAD)
