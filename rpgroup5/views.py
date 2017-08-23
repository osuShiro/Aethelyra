from django.shortcuts import render
from rpgroup5.models import *
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def homepage(request):
    return render(request, 'rpgroup5/home.html')

@login_required(login_url='/login/')
@permission_required('repgroup5.change_chapter',raise_exception=True)
def chapters_admin(request):
    chapter_list=list(Chapter.objects.all())
    return render(request,'rpgroup5/chapters_admin.html', {'chapter_list':chapter_list})

@login_required(login_url='/login/')
@permission_required('rpgroup5.add_chapter',raise_exception=True)
def new_chapter(request):
    if request.method=='GET':
        return render(request, 'rpgroup5/new.html')
    else:
        return HttpResponse('Wtf are you trying to do')

@login_required(login_url='/login/')
@permission_required('rpgroup5.change_chapter',raise_exception=True)
def edit_chapter(request):
    if 'title' not in request.POST or request.POST['title']=='':
        return HttpResponse('No chapter selected.')
    else:
        chapter_title=request.POST['title']
        chapter=Chapter.objects.get(title=chapter_title)
    return render(request,'rpgroup5/chapters_edit.html',{'chapter':chapter})

@login_required(login_url='/login/')
@permission_required('rpgroup5.add_chapter',raise_exception=True)
@permission_required('rpgroup5.change_chapter',raise_exception=True)
@permission_required('rpgroup5.remove_chapter',raise_exception=True)
def success(request, action):
    if action=='add':
        if 'title' not in request.POST or 'content' not in request.POST:
            return HttpResponse('Invalid chapter format (missing title or content).')
        else:
            chapter_title=request.POST['title'].replace(' ', '').replace('\n', '')
            chapter_content=request.POST['content']
            if chapter_title=='' or chapter_title.isspace():
                return HttpResponse('Title cannot be blank.')
            if chapter_content=='' or chapter_content.isspace():
                return HttpResponse('Chapter cannot be empty.')
            existing_chapters=list(Chapter.objects.filter(title=chapter_title))
            if existing_chapters==[]:
                new_chapter=Chapter(title=chapter_title,content=chapter_content)
                new_chapter.save()
                return render(request, 'rpgroup5/success.html', {'action': 'added chapter'})
            else:
                return HttpResponse('Chapter name already exists.')
    elif action=='edit':
        if 'title' in request.POST:
            chapter=Chapter.objects.get(title=request.POST['old_title'])
            chapter.title=request.POST['title'].replace(' ', '').replace('\n', '')
            chapter.save()
            return render(request,'rpgroup5/success.html', {'action': 'changed title'})
        elif 'content' in request.POST:
            if 'chapter_title' not in request.POST:
                return HttpResponse('Chapter not found.')
            else:
                chapter=Chapter.objects.get(title=request.POST['chapter_title'])
                chapter.content=request.POST['content']
                chapter.save()
                return render(request,'rpgroup5/success.html', {'action': 'updated chapter'})
        elif 'delete_title' in request.POST:
            chapter=Chapter.objects.get(title=request.POST['delete_title'])
            chapter.delete()
            return render(request,'rpgroup5/success.html', {'action':'deleted chapter'})
    else:
        return HttpResponse('Action: '+action)

def view_chapter(request):
    chapter_list = list(Chapter.objects.all())
    if request.method=='GET':
        return render(request,'rpgroup5/view.html',{'chapter_list':chapter_list})
    elif request.method=='POST':
        chapter=Chapter.objects.get(title=request.POST['title'])
        return render(request,'rpgroup5/view.html',{'chapter_list':chapter_list,'chapter':chapter})
    else:
        return HttpResponse('Wtf are you trying to do')

def abargia(request):
    return render(request,'rpgroup5/abargia.html')