from rest_framework import generics

from creche.models import JournalEntry
from creche.serializers import (
    ChildSerializer,
    JournalEntryCreateSerializer,
    JournalEntryListSerializer,
    JournalEntryUpdateSerializer,
)


class ChildCreateView(generics.CreateAPIView):
    """Child create view."""

    serializer_class = ChildSerializer


class JournalEntryList(generics.ListCreateAPIView):
    """JournalENtry List or Create view."""

    queryset = JournalEntry.objects.filter(child__is_pupil=True)

    def get_serializer_class(self):
        """
        Get serializer for view.

        If GET request -> get ListSerializer.
        If POST request -> get CreateSerializer.
        :return: Serializer
        """
        if hasattr(self.request, 'method'):
            if self.request.method == 'GET':
                return JournalEntryListSerializer
            if self.request.method == 'POST':
                return JournalEntryCreateSerializer


class JournalEntryDetailUpdate(generics.UpdateAPIView):
    """Journal Entry Update view."""

    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntryUpdateSerializer
