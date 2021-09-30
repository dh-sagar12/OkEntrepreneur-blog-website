from blog.models import BlogComment, Post
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, HttpResponse
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator 
from django.contrib import messages
import datetime 

 
# Create your views here.

def blogHome(request):
    fPost = Post.objects.filter(is_featured=True, is_published=True)[0]
    all_posts = Paginator(Post.objects.filter(is_published= True), 3)
    page = request.GET.get('page')
    try:
        posts = all_posts.page(page)
    except PageNotAnInteger:
        posts = all_posts.page(1)
    except EmptyPage:
        posts = all_posts.page(all_posts.num_pages)
    params = {'allPosts': posts, 'fPost': fPost}
    return render(request, 'blog/blogHome.html', params)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug, is_published= True)[0]
    print(post)
    print(post.post_id)
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    
    #creating a dictionary of all the replies associate to their parent comment where comment id of parent comment will be keys and reply comment will be the value.
    replyDict ={}

    #iterating the replies query set 
    for reply in replies:

        #yadi reply ko parent ko comment id replyDict ko keys ma xaina vane keys ma tyo comment_id ko keys banaune jasma tyo reply as a value rahanxa 
        if reply.parent.comment_id not in replyDict.keys():
            replyDict[reply.parent.comment_id] = [reply]
        
        #yadi pailai tyo dictionary currently iterationg reply ko comment_id ko name bata keys xa vane tesma tyo reply lai append garne
        else:
            replyDict[reply.parent.comment_id].append(reply)
    post.viewsCount += 1
    post.save()
    params = {'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', params)

def search(request):
    query = request.GET.get('query')
    if len(query) <4:
        posts = []
    else:
        allPost = Paginator(Post.objects.filter(Q(slug__icontains= query) | Q(title__icontains= query) | Q(content__icontains= query)), 3)
        editorChoice = Post.objects.all()[:3]
        page = request.GET.get('page')
        try:
            posts = allPost.page(page)
        except PageNotAnInteger:
            posts = allPost.page(1)
        except EmptyPage:
            posts = allPost.page(allPost.num_pages)

    params= {'allPost': posts, 'query':query, 'editorChoice': editorChoice}
    return render(request, 'blog/search.html', params)


def trendingPopular(request, str):
    accept = ['trending', 'popular']
    str = str.lower()
    if str in accept:
        if str == accept[0]:
            weekTime = datetime.date.today() - datetime.timedelta(days= 7)
            allPosts = Paginator(Post.objects.filter(upload_date__gte= weekTime).order_by('-viewsCount'), 3)
        elif str == accept[1]:
            allPosts = Paginator(Post.objects.filter(is_published=True).order_by('-viewsCount'), 3)
        page = request.GET.get('page')
        try:
            posts = allPosts.page(page)
        except PageNotAnInteger:
            posts = allPosts.page(1)
        except EmptyPage:
            posts = allPosts.page(allPosts.num_pages)
        
        params = {'allPost': posts, 'str': str }
        
        return render(request, 'blog/viewall.html', params)
    else:
        return HttpResponse(f'Error 404! page not found')






def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get('post_id')
        post = Post.objects.filter(post_id=post_id).first()
        post.viewsCount -= 1
        post.save()
        parentCommentId = request.POST.get('parentCommentId')
        if parentCommentId == "":
            comments = BlogComment(comment=comment, user=user, post=post)
            comments.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.filter(comment_id = parentCommentId).first()
            print(parent)
            comments = BlogComment(comment=comment, user=user, post=post, parent= parent)
            comments.save()
            messages.success(request, "Your reply has been posted successfully")


    return redirect(f"/blog/{post.slug}")