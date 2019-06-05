from django.shortcuts import render
import markdown
from django.http import HttpResponse
from .models import Article, Category, Tag, Tui, Banner,Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
# 导入分页插件包

def test(request):
    name = "hello haiyan"
    value="<div href=\"\">点击</div>"
    i = 200
    l = [11,22,33,44,55]
    d = {"name":"haiyan","age":20}

    class People(object): #继承元类
        def __init__(self,name,age):
            self.name = name
            self.age = age
        def __str__(self):
            return self.name+str(self.age)
        def dream(self):
            return "你有梦想吗？"
    #实例化
    person_egon = People("egon",10)
    person_dada = People("dada",34)
    person_susan = People("susan",34)
    person_list = [person_dada,person_egon,person_susan]

    return render(request,"test.html",
                    {
                        "name":name,
                        "i":i,
                        "l":l,
                        "d":d,  #键对应的是模板里的名字。值对应的是上面定义的变量
                        "person_egon":person_egon,
                        "person_dada":person_dada,
                        "person_list":person_list,
                    }
              )
    # return render(request,"index.html",locals())
    #用locals()可以不用写上面的render了。不过用locals()，views里面用什么名。模板里面就得用什么名
    # locals()局部的：用了locals就相当于都得按照上面的那样


def global_variable(request):
    rightTui = Article.objects.filter(tui__id=2)[:6]
    alltags = Tag.objects.all()
    allcategory = Category.objects.all()
    return locals()


def categoryPage(request):
    allcategory = Category.objects.all()
    group = []
    nlist = [x for x in range(len(allcategory))]
    for c in allcategory:
        group.append([c, Article.objects.filter(category_id=c.id)[:3], len(Article.objects.filter(category_id=c.id))])
    return render(request, "category.html", locals())


# 首页
def index(request):
    allbanner = Banner.objects.filter(is_active=True)[:4]  # 幻灯片数据
    alltui = Article.objects.filter(tui__id=1)[:3]
    newarticle = Article.objects.all().order_by('-id')[:10]

    # hot = Article.objects.all().order_by('?')[:10] # 随机推荐
    # hot = Article.objects.filter(tui__id=3)[:10]   # 通过自定义推荐进行查询，以推荐ID是3为例
    hotarticle = Article.objects.all().order_by('views')[:6]
    link = Link.objects.all()
    return render(request, "index.html", locals())


# 列表页, 多回传了一个参数，跟urls.py中的对应
def list(request, lid):
    list = Article.objects.filter(category_id=lid)  # 获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)    # 获取当前文章的栏目名

    #page = request.GET.get('page')  # 在URL中获取当前页面数
    #paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    #try:
        #list = paginator.page(page)     # 获取当前页码的记录
    #except PageNotAnInteger:
        #list = paginator.page(1)    # 如果用户输入的页码不是整数时,显示第1页的内容
    #except EmptyPage:
        #list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'list.html', locals())   # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典。


# 内容页
def show(request, sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    hot = Article.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    curcategory = Article.objects.filter(category=show.category)
    previous_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    next_blog = Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    show.body = markdown.markdown(show.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.toc',
                                      'markdown.extensions.codehilite',
                                  ])
    return render(request, 'show.html', locals())


# 标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)  # 获取通过URL传进来的tag，然后筛选出对应文章
    tname = Tag.objects.get(name=tag)    # 获取当前文章的栏目名

    # page = request.GET.get('page')  # 在URL中获取当前页面数
    # paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    # try:
        # list = paginator.page(page)     # 获取当前页码的记录
    # except PageNotAnInteger:
        # list = paginator.page(1)    # 如果用户输入的页码不是整数时,显示第1页的内容
    # except EmptyPage:
        # list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'tags.html', locals())   # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典。


# 搜索页
def search(request):
    ss=request.GET.get('search')    # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配

    page = request.GET.get('page')
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())


# 关于我们
def about(request):
    allcategory = Category.objects.all()
    return render(request, 'about.html', locals())

# 该作者
def author(request):
    # list = Article.objects.all().order_by('created_time').reverse()
    list = Article.objects.all() # .order_by('created_time').reverse()
    return render(request, 'author.html', locals())

# 友情链接
def link(request):
    allcategory = Category.objects.all()
    return render(request, 'link.html', locals())


# 书单
def book(request):
    allcategory = Category.objects.all()
    return render(request, 'book.html', locals())


# 分类页面
def category(request):
    allcategory = Category.objects.all()
    return render(request, 'category.html', locals())


# 表单
def search_form(request):
    return render(request, 'search_form.html')
 
# 接收请求数据
def search(request):  
    request.encoding='utf-8'
    if 'q' in request.GET:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)

# 接收POST请求数据
def search_post(request):

    headers = ['title1', 'excerpt1','viewscount1', 'user1']
    headers2 = ['title2', 'category2','tag2']

    list = Article.objects.all()
    list2 = Article.objects.all()
    if request.POST:
        if 'title1' in request.POST and request.POST['title1']:
            list = list.filter(title__icontains=request.POST['title1'])  # 标题包含文字
        if 'excerpt1' in request.POST and request.POST['excerpt1']:
            list = list.filter(excerpt__icontains=request.POST['excerpt1'])  # 标题包含文字
        if 'viewscount1' in request.POST and request.POST['viewscount1']:
            list = list.filter(views__gt=request.POST['viewscount1'])  # 浏览量
        if 'user1' in request.POST and request.POST['user1']:
            list = list.filter(user=request.POST['user1'])  # 标题包含文字

        if 'title2' in request.POST and request.POST['title2']:
            list2 = list2.filter(title__icontains=request.POST['title2'])  # 标题包含文字
        if 'category2' in request.POST and request.POST['category2']:
            list2 = list2.filter(category__name__icontains=request.POST['category2'])  # 标题包含文字
        if 'tag2' in request.POST and request.POST['tag2']:
            print(type(request.POST['tag2']))
            taglist = request.POST['tag2'].split(' ')
            print(taglist)
            for foo in taglist:
                list2 = list2.filter(tags__name__icontains=foo)

    return render(request, "post.html", locals())


def search_post3(request):
    headers3 = ['title3', 'excerpt3', 'category3']
    headers4 = ['blog_id', 'tag_id']
    headers5 = ['blog_id5', 'title5']
    headers6 = ['blog_id6', 'title6', 'excerpt6', 'category6']
    if request.POST:
        if 'title3' in request.POST:
            if len(request.POST['title3']) and len(request.POST['excerpt3']) and len(request.POST['category3']):
                Article.objects.create(title=request.POST['title3'], excerpt=request.POST['excerpt3'], category_id=request.POST['category3'], img='https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80', body='这是新增加的一篇博客', user_id=2)
        if 'blog_id' in request.POST:
            if len(request.POST['blog_id']) and len(request.POST['tag_id']):
                blog = Article.objects.get(id=request.POST['blog_id'])
                taglist = request.POST['tag_id'].split(' ')
                for foo in taglist:
                    addTag = Tag.objects.get(id=foo)
                    blog.tags.add(addTag)
        if 'blog_id5' in request.POST or 'title5' in request.POST:
            if request.POST['blog_id5']:
                blog = Article.objects.get(id=request.POST['blog_id5']).delete()
            if request.POST['title5']:
                blog = Article.objects.filter(title__icontains=request.POST['title5']).delete()
        if 'blog_id6' in request.POST and request.POST['blog_id6']:
            blog = Article.objects.get(id=request.POST['blog_id6'])
            if request.POST['title6']:
                blog.title = request.POST['title6']
            if request.POST['excerpt6']:
                blog.excerpt = request.POST['excerpt6']
            if request.POST['category6']:
                blog.category_id = request.POST['category6']
            blog.save()

    allcategorys = Category.objects.all()
    alltags = Tag.objects.all()
    list = Article.objects.all()
    return render(request, "post3.html", locals())
