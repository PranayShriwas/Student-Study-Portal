from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('/notes/', views.notes, name='notes'),
    path('delete_notes/<int:pk>', views.delete_note, name='delete_note'),
    path('notes_detail/<int:pk>',
         views.NotesDetailView.as_view(), name='note-detail'),
    path('notedetail/<int:pk>', views.notedetail, name='notedetail'),
    path('/homework/', views.homework, name='homework'),
    path('deletehomework/<int:pk>', views.delete_homework, name='deletehomework'),
    path('updatehomework/<int:pk>', views.update_homework, name='update_homework'),
    path('/youtube', views.youtube, name='youtube'),
    path('/todo/', views.todo, name='todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete_todo'),
    path('/books/', views.books, name='books'),
    path('/dictionary/', views.dictionary, name='dictionary'),
    path('/wiki/', views.wiki, name='wiki'),
    path('/conversion/', views.conversion, name='conversion'),



]
