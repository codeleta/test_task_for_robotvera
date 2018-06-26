from datetime import datetime

from rest_framework import serializers

from creche.models import Child, JournalEntry


def get_now_time():
    """Get now date."""
    return datetime.now().time()


def get_now_date():
    """Get now time."""
    return datetime.now().date()


class ChildSerializer(serializers.ModelSerializer):
    """Serializer for ChildEntry."""

    class Meta:
        model = Child
        fields = '__all__'


class JournalEntryListSerializer(serializers.ModelSerializer):
    """Serializer for list JournalEntry."""

    class Meta:
        model = JournalEntry
        fields = '__all__'


class JournalEntryCreateSerializer(serializers.ModelSerializer):
    """Serializer for create JournalEntry."""

    timestamp_come = serializers.HiddenField(default=serializers.CreateOnlyDefault(get_now_time))
    datestamp = serializers.HiddenField(default=serializers.CreateOnlyDefault(get_now_date))

    class Meta:
        model = JournalEntry
        fields = ('id', 'child', 'datestamp', 'timestamp_come', 'people_come')


class JournalEntryUpdateSerializer(serializers.ModelSerializer):
    """Serializer for update JournalEntry."""

    timestamp_away = serializers.HiddenField(default=get_now_time)
    datestamp = serializers.DateField(read_only=True)
    child = serializers.PrimaryKeyRelatedField(read_only=True)
    people_away = serializers.ChoiceField(required=True, choices=JournalEntry.PEOPLES.CHOICES)

    class Meta:
        model = JournalEntry
        fields = ('id', 'child', 'datestamp', 'timestamp_away', 'people_away')
