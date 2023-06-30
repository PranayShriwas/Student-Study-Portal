from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('delete_notes/<int:pk>', views.delete_note, name='delete_note'),
    path('notes_detail/<int:pk>',
         views.NotesDetailView.as_view(), name='note-detail'),
    path('notedetail/', views.notedetail, name='notedetail')
]