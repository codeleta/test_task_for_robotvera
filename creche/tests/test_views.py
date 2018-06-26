from django.test import TestCase

from creche.views import (
    ChildCreateView,
    JournalEntryDetailUpdate,
    JournalEntryList,
)


class ViewsTest(TestCase):
    """Tests views allowed methods."""

    @staticmethod
    def get_allowed_methods(view_class):
        """
        Return allowed methods for view class.

        :param view_class: class of view.
        :return: List[str]
        """
        return sorted(view_class._allowed_methods(view_class()))

    def test_journal_list_create_view_methods(self):
        """Check correct allowed methods for JournalEntryList."""
        self.assertEqual(self.get_allowed_methods(JournalEntryList), sorted(['GET', 'POST', 'OPTIONS']))

    def test_journal_update_view_methods(self):
        """Check correct allowed methods for JournalEntryDetailUpdate."""
        self.assertEqual(self.get_allowed_methods(JournalEntryDetailUpdate), sorted(['PUT', 'PATCH', 'OPTIONS']))

    def test_child_create_view_methods(self):
        """Check correct allowed methods for ChildCreateView."""
        self.assertEqual(self.get_allowed_methods(ChildCreateView), sorted(['POST', 'OPTIONS']))
