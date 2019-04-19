from django.shortcuts import render
import markdown
from django.http import HttpResponse
from .models import Article, Category, Tag, Tui, Banner,Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    list = Article.objects.all().order_by('created_time').reverse()
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
