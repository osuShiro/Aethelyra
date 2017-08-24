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
            chapter_title=request.POST['title'].replace(' ', '_').replace('\n', '_')
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

@login_required(login_url='/login/')
@permission_required('rpgroup5.add_sessionlog',raise_exception=True)
@permission_required('rpgroup5.change_sessionlog',raise_exception=True)
@permission_required('rpgroup5.remove_sessionlog',raise_exception=True)
def chatlog_admin(request):
    if request.method=='GET':
        return render(request,'rpgroup5/chatlogs_admin.html')
    elif request.method=='POST':
        if 'group' in request.POST:
            group=request.POST['group']
            chatlog_list=list(SessionLog.objects.filter(rp_group=group.lower()))
            return render(request,'rpgroup5/chatlogs_admin.html', {'group':group, 'chatlog_list':chatlog_list})
    else:
        render(Http404)

@login_required(login_url='/login/')
@permission_required('rpgroup5.add_sessionlog',raise_exception=True)
@permission_required('rpgroup5.change_sessionlog',raise_exception=True)
@permission_required('rpgroup5.remove_sessionlog',raise_exception=True)
def chatlog_edit(request, group):
    if 'title' not in request.POST or request.POST['title']=='':
        return HttpResponse('No chatlog selected.')
    else:
        chatlog_title=request.POST['title']
        chatlog = SessionLog.objects.get(title=chatlog_title, rp_group=group.lower())
        if chatlog:
            pass
        else:
            return HttpResponse(group)
    return render(request,'rpgroup5/chatlogs_edit.html',{'chatlog':chatlog})

def chatlog_success(request,group,action):
    if action=='add':
        if 'title' not in request.POST or 'content' not in request.POST or 'group' not in request.POST:
            return HttpResponse('Invalid chapter format (missing title, group or content).')
        else:
            chatlog_title=request.POST['title'].replace(' ', '_').replace('\n', '_')
            chatlog_content=request.POST['content']
            chatlog_group=request.POST['group'].lower()
            if chatlog_title=='' or chatlog_title.isspace():
                return HttpResponse('Title cannot be blank.')
            if chatlog_content=='' or chatlog_content.isspace():
                return HttpResponse('Chatlog cannot be empty.')
            existing_chatlogs=list(SessionLog.objects.filter(rp_group=chatlog_group, title=chatlog_title))
            if existing_chatlogs==[]:
                new_chatlog=SessionLog(rp_group=chatlog_group, title=chatlog_title, content=chatlog_content)
                new_chatlog.save()
                return render(request, 'rpgroup5/chatlog_success.html', {'action': 'added chatlog'})
            else:
                return HttpResponse('Chapter name already exists.')
    elif action=='edit':
        if 'title' in request.POST:
            chatlog=SessionLog.objects.get(rp_group=group.lower(), title=request.POST['old_title'])
            chatlog.title=request.POST['title'].replace(' ', '').replace('\n', '')
            chatlog.save()
            return render(request,'rpgroup5/chatlog_success.html', {'action': 'changed title'})
        elif 'content' in request.POST:
            if 'chatlog_title' not in request.POST:
                return HttpResponse('Chatlog not found.')
            else:
                chatlog=SessionLog.objects.get(rp_group=group.lower(), title=request.POST['chatlog_title'])
                chatlog.content=request.POST['content']
                chatlog.save()
                return render(request,'rpgroup5/chatlog_success.html', {'action': 'updated chatlog'})
        elif 'delete_title' in request.POST:
            chatlog = SessionLog.objects.get(title=request.POST['delete_title'], rp_group=group.lower())
            if chatlog:
                chatlog.delete()
                return render(request, 'rpgroup5/success.html', {'action': 'deleted chapter'})
            else:
                return HttpResponse('Could not find chatlog to delete.')
    else:
        return HttpResponse('Wtf are you trying to do<br />'+action)

@login_required(login_url='/login/')
@permission_required('rpgroup5.add_sessionlog', raise_exception=True)
def new_chatlog(request):
    if request.method == 'GET':
        return render(request, 'rpgroup5/chatlog_new.html')
    else:
        return HttpResponse('Wtf are you trying to do')

def abargia(request):
    return render(request,'rpgroup5/abargia.html')