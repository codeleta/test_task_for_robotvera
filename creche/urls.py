from django.urls import path

from .views import ChildCreateView, JournalEntryDetailUpdate, JournalEntryList

urlpatterns = [
    path('child/', ChildCreateView.as_view()),
    path('journal/', JournalEntryList.as_view()),
    path('journal/<int:pk>/', JournalEntryDetailUpdate.as_view()),
]
