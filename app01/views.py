from django.shortcuts import render,redirect,HttpResponse  # 跳转，重定向，响应
from app01.models import Book,Author,Publish,Author_info,User_info  # 导入模型表
from django.urls import reverse  # 反向解析
from django.core.paginator import Paginator,EmptyPage   # 分页器
from django.contrib import auth  # auth认证组件
from django.contrib.auth.models import User  # auth认证组件
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError  # forms 错误
from django.forms import widgets    #
from django import forms        # forms 组件
from django.http import JsonResponse  # 返回json数据
# Create your views here.
def login(request):
    '''
    登陆视图函数:
        1.判断请求的类型 POST & GET;
        2.GET请求跳转login.html,POST请求接收Ajax数据;
        3.验证信息,判断验证码、用户名及密码是否正确,错误返回错误信息;
    :param request:
    :return:
    '''
    import json
    res = {"success":None,"error":None}
    if request.method=='GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        validcode = request.POST.get('validcode')
        print(username,password,validcode)
        if validcode.upper() != request.session.get("keep_str").upper():
            res['error'] = '验证码输入错误'
            return HttpResponse(json.dumps(res))
        user_obj = auth.authenticate(username=username,password=password)
        print(user_obj) #用户名
        if user_obj:
            print("success")
            auth.login(request, user_obj) # 保存用户状态
            res['success']=200
            return HttpResponse(json.dumps(res))
        else:
            print("error")
            res['error'] = '用户名或密码错误'
            return HttpResponse(json.dumps(res))

def get_valid_img(request):
    '''
    验证码视图函数:
        1.定义随机三原色函数
        2.导入图片处理模块，定义画板、文本
        3.读与写（内存中）,将验证码保存在各自的session中
    :param request:
    :return:
    '''
    import random
    def get_random_color():
        '''
        随机三原色:
            返回三个0-255的值
        :return:
        '''
        return (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
    # 需要下载图片处理模块 pip3 install pillow
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO

    img = Image.new("RGB", (555, 50), get_random_color())   # Image.new（） 三个值  （模式，长宽，数值)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/kumo.ttf", 48)

    keep_str = ""
    for i in range(6):
        random_num = str(random.randint(0, 9))
        random_lowalf = chr(random.randint(97, 122))
        random_upperalf = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_lowalf, random_upperalf])
        draw.text((i * 50 + 150, 0), random_char, get_random_color(), font=font)
        keep_str += random_char
    # 写与读
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    print('keep_str', keep_str)
    # 将验证码存在各自的session中
    request.session['keep_str'] = keep_str
    return HttpResponse(data)
def logout(request):
    '''
    注销视图函数:
        清除cookie中的键值
    :param request:
    :return:
    '''
    auth.logout(request)

    return redirect("/login/")

def setpwd(request):
    '''
        修改密码视图函数:
            1.判断请求的类型 POST & GET;
            2.GET请求跳转页面,POST请求接收Ajax数据;
            3.验证信息,判断两次密码输入是否一致,错误返回错误信息,正确获取用户名,设置密码并保存;
        :param request:
        :return:
        '''
    import json
    res = {"success": None, "error": None}
    if request.method == 'GET':
        return render(request, 'setpwd.html')
    else:
        print('ok')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password1)
        if password1 ==password2:
            print("success")
            user=User.objects.get(username=request.user.username) #获取用户名
            user.set_password(raw_password=password1)  # 设置密码
            user.save()     # 保存密码
            res['success'] = 200
            return HttpResponse(json.dumps(res))
        else:
            print("error")
            res['error'] = '两次密码输入不相同，请重新输入'
            return HttpResponse(json.dumps(res))


    # user=User.objects.get(username=request.user.username)
    # user.set_password(raw_password="666")
    # user.save()



class UserForm(forms.Form):
    '''
    forms组件应用函数:
        1.设置字段校验信息
        2.定义局部钩子，二次校验，错误返回错误信息
        3.定义全局钩子，再次校验，错误返回错误信息
    '''
    msg={"required":"该字段不能为空",'max_length':'太长了',
                         'min_length':'太短了',}
    username=forms.CharField(min_length=5,
                         label="用户名",
                         error_messages=msg,
                         widget=widgets.TextInput(attrs={"class":"form-control"})
                         )
    password=forms.CharField(error_messages=msg,
                           label="密码",
                          widget=widgets.PasswordInput(attrs={"class":"form-control"})
                           )
    re_password = forms.CharField(error_messages=msg,
                          label="确认密码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"})
                          )


    email=forms.EmailField(error_messages={"invalid":"邮箱格式错误","required":"该字段不能为空"},
                           label="邮箱",
                           widget=widgets.EmailInput(attrs={"class":"form-control"})
                           )

    def clean_username(self):
        val=self.cleaned_data.get("username")
        ret=User_info.objects.filter(user=val).first()
        if not ret:
            return val
        else:
            raise ValidationError("用户名已存在！")

    def clean_password(self):
        val=self.cleaned_data.get("password")
        if val.isdigit():
            raise ValidationError("密码不能是纯数字！")
        else:
            return val


    # 校验邮箱格式
    def clean_email(self):
        import re
        rul = re.compile('\w[-\w.+]*@([1][6][3]+\.)+[A-Za-z]{2,14}')
        val = self.cleaned_data.get("email")
        ret = re.search(rul,val)
        if ret == None:
            raise ValidationError("163邮箱格式错误！")
        else:
            return val
    def clean(self):
        password=self.cleaned_data.get("password")
        re_password=self.cleaned_data.get("re_password")
        if password and re_password:
            if password==re_password:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致!')
        else:
            return self.cleaned_data
def register(request):
    '''
    注册视图函数:
        1.判断请求的类型 POST & GET;
        2.GET请求跳转至页面,POST请求接收Ajax数据(request.body)
        3.实例化UserForm对象,判断是否通过校验(is_valid()),通过在auth_user表中创建数据(注意create_user),没通过返还错误信息.
    :param request:
    :return:
    '''
    import json
    # res = {"success": None, "error": None}
    msg = {'info':None}
    if request.method == "GET":
        form = UserForm()
        return render(request, "register.html",locals())
    else:
        data = json.loads(request.body)
        print(data)
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # print(username,password)
        # user_obj = auth.authenticate(username=username)
        # print(user_obj)
        # # if user_obj:
        # #     print("error")
        # #     res['error'] = '用户名已存在'
        # #     return HttpResponse(json.dumps(res))
        # # else:
        # User.objects.create_user(username=username, password=password)
        # res['success'] = 200
        form = UserForm(data)  # 实例化对象
        # print(form)
        if form.is_valid():  # 判断是否通过验证
            print(form.cleaned_data)
            print('success')
            del form.cleaned_data['re_password'] # 删除不必要的字段
            User.objects.create_user(**form.cleaned_data) # 将数据打散传输
        else:
            js_dict={}
            for i,j in form.errors.items():
                js_dict[i]=j[0]
            msg['info']=js_dict

            # print(form.cleaned_data)
            # print(form.errors) # {"user":["",]}
            # print(form.errors.get("user")[0]) # {"user":["",]}
        js_msg = json.dumps(msg)
        return HttpResponse(js_msg)






def index(request):
    print(request.user)  # 默认匿名用户对象 AnonymousUser
    print(request.user.id)  # None
    print(request.user.username)  # ""
    print(request.user.is_active)  # False
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:   # 有没有登陆
        return redirect("/login/")
    username = request.user.username
    book_list = Book.objects.all()
    paginator = Paginator(book_list,13)  # 设置每页显示多少个
    try:
        current_page_num = request.GET.get('page',1)
        current_page = paginator.page(current_page_num)
    except EmptyPage as e:
        current_page_num = 1
        current_page = paginator.page(1)
    page_num = (int(current_page_num)-1)*13
    return render(request,'index.html',{'page_num':page_num,"book_list":book_list,'paginator':paginator,'current_page_num':int(current_page_num),'current_page':current_page,'username':username})
def give(request):
    import os
    from bms2 import settings
    file_obj = request.FILES.get("file_obj")
    filename = file_obj.name
    abs_path =os.path.join(settings.BASE_DIR,"media","img",filename)
    print(abs_path)
    with open(abs_path,"wb") as f:
        for line in file_obj:
            f.write(line)

    return HttpResponse('ok')
def page(request):
    # 任何请求都会通过中间件
    pass
    # from django.core.paginator import Paginator, EmptyPage
    # book_list = Book.objects.all()
    # paginator = Paginator(book_list, 20)  # 设置每页显示多少个
    # try:
    #     current_page_num=request.GET.get("page",1) # 加载页面显示第一页
    #     # print(current_page_num)
    #     current_page=paginator.page(current_page_num)
    # except EmptyPage as e:
    #     current_page_num=1
    #     current_page = paginator.page(1)
    # return render(request,"page.html",{"current_page":current_page,"paginator":paginator,"current_page_num":int(current_page_num)})
def setup(request):
    # book_list = []
    #
    # for i in range(100):
    #     book = Book(bname="book_%s" % i, price=i * i,pub_date='2012-12-12',publish_id='2')
    #     book_list.append(book)
    #
    # Book.objects.bulk_create(book_list)

    return render(request,'setup.html')
def add(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method=='POST':
        bname = request.POST.get('bname')
        price = request.POST.get('price')
        pub_date = request.POST.get('pub_date')
        publish_id = request.POST.get('publish_id')
        authors = request.POST.getlist('authors')
        book = Book.objects.create(bname=bname, price=price, pub_date=pub_date, publish_id=publish_id)
        book.authors.add(*authors)
        return redirect("/index/")
    else:
        publish_list = Publish.objects.all()
        author_list = Author.objects.all()
        return render(request, "add.html", {"publish_list": publish_list, "author_list": author_list})

def update(request,edit_book_id):
    if not request.user.is_authenticated:
        return redirect("/login/")
    edit_book = Book.objects.filter(pk=edit_book_id).first()
    if request.method == "GET":
        publish_list = Publish.objects.all()
        author_list = Author.objects.all()
        return render(request, "update.html",
                      {"edit_book": edit_book, "publish_list": publish_list, "author_list": author_list})

    else:
        bname = request.POST.get("bname")
        price = request.POST.get("price")
        pub_date = request.POST.get("pub_date")
        publish_id = request.POST.get("publish_id")
        authors = request.POST.getlist("authors")
        Book.objects.filter(pk=edit_book_id).update(bname=bname, price=price, pub_date=pub_date, publish_id=publish_id)
        edit_book.authors.set(authors)

        return redirect("/index/")
def delete(request,del_book_id):
    import json
    res = {'success':None , 'error': None}
    if not request.user.is_authenticated:
        res['error']=200
        ret =json.dumps(res)
    else:
        res['success']=True
        Book.objects.filter(pk=del_book_id).delete()
        ret =json.dumps(res)
    return HttpResponse(ret)

def select(request):
    # 查询'瓜皮'这本书的出版社名字
    '''
        select pname from app01_book INNER JOIN app01_publish on app01_book.publish_id = app01_publish.pid where bname = '瓜皮';

    '''
    # 方式一
    # ret = Publish.objects.filter(book__bname='瓜皮').values('pname')
    # 方式二
    # ret = Book.objects.filter(bname='瓜皮').values('publish__pname')

    # 查询**出版社出版的所有的书籍的名称
    # ret = Book.objects.filter(publish__pname='英国').values('bname')
    ret = Publish.objects.filter(pname='美国').values('book__bname')    # 反向查询 表名小写__字段

    print(ret)
    return HttpResponse('OK')



def index2(request):
    author_list = Author.objects.all()
    return render(request,'index2.html',{'author_list':author_list})

def add2(request):
    if request.method=='POST':
        addr = request.POST.get('addr')
        tel = request.POST.get('tel')
        Au_Info=Author_info.objects.create(addr=addr,tel=tel)
        aname = request.POST.get('aname')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        Author.objects.create(aname=aname,age=age,phone=phone,a_info_id=Au_Info.pk)
        return redirect(reverse('index2'))
    else:
        return render(request,'add2.html')
def update2(request,id):
    if request.method=='POST':
        aname = request.POST.get('aname')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        a_info_id= id
        addr = request.POST.get('addr')
        tel = request.POST.get('tel')
        Author_info.objects.filter(pk=a_info_id).update(addr=addr,tel=tel)
        Author.objects.filter(pk=a_info_id).update(aname=aname,age=age,phone=phone)
        return redirect("/index2/")
    else:
        author = Author.objects.filter(aid=id).first()
        print(author)
        return render(request, 'update2.html',{'author':author})
def delete2(request,id):
    Author_info.objects.filter(pk=id).delete()
    return redirect("/index2/")







################################################################################
# 基于modelform组件
from django.forms import widgets as wid
class ModelForm(forms.ModelForm):
    '''
    1.定义Meta类，创建model=表字段，fields='__all__'
    2.设置与定义
    '''
    class Meta:
        model=Publish
        fields="__all__"
        # fields=["title","price","pub_date"]
        # exclude=["title"]
        labels={
            "pname":"出版社名字",
            "email":"邮箱地址"
        }
        error_messages={
            "pname":{"required":"不能为空"}
        }
        # widgets={
        #     "pub_date":wid.TextInput(attrs={"type":"date"})
        # }

    def clean_price(self):
        # 定义局部钩子
        pass
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for filed in self.fields.values():
            #filed.error_messages={"required":"不能为空"}
            filed.widget.attrs.update({'class': 'form-control'})




def index3(request):
    publish_list = Publish.objects.all()
    print(publish_list)
    return render(request,'index3.html',{'publish_list':publish_list})

def add3(request):

    if request.method=='POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            # authors=form.cleaned_data.pop("authors")
            # book = Book.objects.create(**form.cleaned_data)
            # book.authors.add(*authors)
            obj = form.save()  # create
            return redirect("/index3/")
        else:

            return render(request, "add.html", {"form": form})

    else:
        form = ModelForm()
        return render(request, "add3.html", {"form": form})
def update3(request,id):
    re_Publish = Publish.objects.filter(pk=id).first()
    if request.method == "GET":

        form = ModelForm(instance=re_Publish)
        return render(request, "update3.html", {"form": form})

    else:
        form = ModelForm(request.POST, instance=re_Publish)
        if form.is_valid():
            form.save()  # update操作 ;  edit_book.update(**cleandata)
            return redirect("/index3/")
        else:
            return render(request, "update3.html", {"form": form})

def delete3(request,id):
    Publish.objects.filter(pk=id).delete()
    return redirect("/index3/")