import re
import copy

# ##################### 定制插件（HTMl）  #####################
class TextInput(object):
    """
    定制前端页面的标签：
    :return: <input type='text' class="c1" ID='I1' ..../>"
    """
    def __init__(self,attrs=None):
        """
        标签自定制属性功能
        :param attrs: {'class':'c1', .....}
        """
        if attrs:
            self.attrs = attrs
        else:
            self.attrs = {}

    def __str__(self):

        data_list = []
        for k,v in self.attrs.items():
            tmp = "{0}='{1}'".format(k,v)
            data_list.append(tmp)
        tpl = "<input type='text' {0}>".format(" ".join(data_list))
        return tpl


class EmailInput(object):

    def __init__(self, attrs=None):
        if attrs:
            self.attrs = attrs
        else:
            self.attrs = {}

    def __str__(self):

        data_list = []
        for k, v in self.attrs.items():
            tmp = "{0}='{1}'".format(k, v)
            data_list.append(tmp)
        tpl = "<input type='email' {0} />".format(" ".join(data_list))
        return tpl


class PasswordInput(object):

    def __init__(self, attrs=None):
        if attrs:
            self.attrs = attrs
        else:
            self.attrs = {}

    def __str__(self):

        data_list = []
        for k, v in self.attrs.items():
            tmp = "{0}='{1}'".format(k, v)
            data_list.append(tmp)
        tpl = "<input type='password' {0} />".format(" ".join(data_list))
        return tpl

# ##################### 定制字段（正则）  #####################
class Field(object):

    def __str__(self):
        """
        保存用户输入的值，当用户调用过is_valid,则self.value有值，
        在插件中增加属性 value = 用户提交过来的值
        :return: 插件的str值，验证过则新增value = 输入值的属性
        """
        if self.value:
            self.widget.attrs['value'] = self.value

        return str(self.widget)


class CharField(Field):
    default_widget = TextInput
    regex = "\w+"

    def __init__(self,widget=None):
        """
        初始化的时候，设置对应的插件，如果传入widget,则使用widget传入的插件对象，
        如果未传入则使用默认的插件对象。
        :param widget: 插件对象，TextInput()、EmailInput()....
        """
        self.value = None
        self.widget = widget if widget else self.default_widget()

    def valid_field(self,value):
        self.value = value
        if re.match(self.regex,value):
            return True
        else:
            return False


class EmailField(Field):
    default_widget = EmailInput
    regex = "\w+@\w+"

    def __init__(self,widget=None):
        self.value = None
        self.widget = widget if widget else self.default_widget()

    def valid_field(self,value):
        self.value = value
        if re.match(self.regex,value):
            return True
        else:
            return False

# ##################### 定制Form  #####################
class BaseForm(object):

    def __init__(self,data):
        """
        获取在类中生成的所有插件，设置到对象中，并添加到self.fields字典中，
        供is_valid方法对所有注册的插件进行数据验证。
        :param data:
        """
        self.fields = {}
        self.data = data   #用户form表单提交值 {"user":'Mitsui','email':'Mitsui@live.com'}
        #需要使用Form表单时，会继承BaseForm类，实例化生成对象时，self即需要在前端展示的form对象
        #通过type(self)找到Form类，Form类__dict__中包含所有的类的静态字段，即使用form时创建的插件，
        #user = CharField() 插件都是继承自Field类，由此获取所有的插件
        for name,field in type(self).__dict__.items():
            #name:user,    field:CharField()
            if isinstance(field,Field):
                #由于是静态字段，所以使用的是同一个对象，如果对其进行修改，会影响其它的form对象，
                #所以这里通过深拷贝防止对其进行修改
                new_field = copy.deepcopy(field)
                #将类的这些静态字段设置到对象中，方便调用
                setattr(self,name,new_field)
                self.fields[name] = new_field

    def is_valid(self):
        """
        将form组件设置的所有字段循环，交给每一个Field字段验证，如果有一个错误
        返回False,否则返回True
        :return:
        """
        flag = True
        for name,field in self.fields.items():
        # name:user,    field:CharField()
            user_input_val = self.data.get(name)
            result = field.valid_field(user_input_val)
            if not result:
                flag = False
        return flag

# #####################  使用Form #####################

class LoginForm(BaseForm):
    user = CharField()
    email = EmailField(widget=EmailInput())

#Django:
# if request == "GET":
#     form = LoginForm()
#     return render('login.html',{'form':form})
# else:
#     form = LoginForm(request.POST)
#     if form.is_valid():
#         pass
#     else:
#         pass
l
# Tornado:
# def get(self, *args, **kwargs):
#     form = LoginForm()
#     self.render("login.html",form=form)
#
# def post(self, *args, **kwargs):
#     post_data = {}
#     for key in self.request.arguments:
#         if key == '_xsrf': continue
#         post_data[key] = self.get_arguments(key)[0]
#     form = LoginForm(post_data)
#     if form.is_valid():
#         pass
#     else:
#         self.render('login.html',form=form)




