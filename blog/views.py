from django.shortcuts import render
import markdown
from django.http import HttpResponse
from .models import Article, Category, Tag, Tui, Banner,Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 导入分页插件包


def global_variable(request):
    rightTui = Article.objects.filter(tui__id=2)[:6]
    alltags = Tag.objects.all()
    allcategory = Category.objects.all()
    return locals()


def hello(request):
    return HttpResponse('欢迎使用Django！')


def index_pre(request):
    sitename = 'iTT个人博客网站'
    url = 'hooray1998.github.io/note'
    list=[
            '开发前的准备',
            '项目需求分析',
            '数据库设计分析',
            '创建项目',
            '基础配置',
            '欢迎界面',
            '创建数据库模型',
            ]
    mydict={
            'name': '朱亚非',
            'QQ': '1165131346',
            'github': 'github.com/hooray1998',
            'email': 'hoorayitt@gmail.com',
            }

    allarticle = Article.objects.all()

    context = {
        'sitename': sitename,
        'url': url,
        'list': list,
        'mydict': mydict,
        'allarticle': allarticle,
    }
    return render(request, 'index.html', context)


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

    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)     # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)    # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'list.html', locals())   # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典。


# 内容页
def show(request, sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    hot = Article.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    curcategory = Article.objects.filter(category=show.category)[:3]
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
    tnums = len(list)

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
