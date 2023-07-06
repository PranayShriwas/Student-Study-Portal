from django.shortcuts import render, redirect
from .froms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
# Create your views here.


def home(request):
    return render(request, 'home.html')


def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(
            request, f'Notes Added from {request.user.username} SuccessFully!')

    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


def notedetail(request, pk):
    note = Notes.objects.filter(id=pk)
    return render(request, 'notes_detail.html', {'note': note})


class NotesDetailView(generic.DetailView):
    model = Notes


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(
                request, f'Homework Added From {request.user.username}!!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks': homework,
               'homework_done': homework_done, 'form': form}
    return render(request, 'homework.html', context)


def delete_homework(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnails': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'publishedTime': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'youtube.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'youtube.html', context)


def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.Post)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(
                request, f'Todo Added From {request.user.username}!!')
    else:
        form = TodoForm
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'todos': todo,
        'form': form,
        'todos_done': todos_done
    }
    return render(request, 'todo.html', context)


def delete_todo(request, pk):
    Todo.objects.get(pk=pk).delete()
    return redirect('todo')


# def books(request):
#     form = DashboardForm()
#     context = {'form': form}
#     return render(request, 'books.html', context)


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {

                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),


            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'books.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['phonetics'][0]['definitions'][0]['definition']
            example = answer[0]['phonetics'][0]['definitions'][0]['example']
            synonyms = answer[0]['phonetics'][0]['definitions'][0]['sunonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': '',
            }
        return render(request, 'dictionary.html', context)

    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'wiki.html', context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['messurement'] == 'length':
            messurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': messurement_form,
                'input': True
            }
            if 'input' in request:
                first = request.POST['messure1']
                second = request.POST['messure2']
                input = request.POSt['input']
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard={int(input)*3}foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} yard={int(input)/3}yard'
                context = {
                    'form': form,
                    'm_form': messurement_form,
                    'input': True,
                    'answer': answer
                }
        if request.POST['messurement'] == 'mass':
            messurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': messurement_form,
                'input': True
            }
            if 'input' in request:
                first = request.POST['messure1']
                second = request.POST['messure2']
                input = request.POSt['input']
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound={int(input)*0.453592}kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram={int(input)/2.2062}pound'
                context = {
                    'form': form,
                    'm_form': messurement_form,
                    'input': True,
                    'answer': answer
                }

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
    return render(request, 'conversion.html', context)


def profile(request):
    return render(request, 'profile.html')
