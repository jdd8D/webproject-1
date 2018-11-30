import urllib.request
import urllib.parse
import re

from django.shortcuts import render,redirect,render_to_response
from django.conf import settings
from django.http import JsonResponse
import logging
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm

from webapp.forms import *
from webapp.models import *

logger = logging.getLogger('webapp.views')

def authenticated_view(function):
  def wrap(request, *args, **kwargs):
      if request.user.is_authenticated():
          return function(request)
      else:
        login_form = LoginForm()
        return render(request, 'login.html', locals())

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap

# Create your views here.

def global_setting(request):
    
    MEDIA_URL = settings.MEDIA_URL
    difficulty_list = Difficulty.objects.all()
    cart = request.session.get(request.user.id, None)
    return locals()

#home page
def index(request):
    techno_list = Technology.objects.filter(show = True)
    techno_list = getPage(request,techno_list)
    return render(request,"index2.html",locals())

########################################################################################
def difficulties(request):
    try:
        did = request.GET.get('did',None)
        try:
            difficulty = Difficulty.objects.get(pk=did)
        except Difficulty.DoesNotExist:
            return render(request, 'error.html', {"reason":"Difficulté n'existe pas!"})
        techno_list = Technology.objects.filter(difficulty = difficulty, show = True)
        techno_list = getPage(request,techno_list)
        need_list = Need.objects.filter(difficulty = difficulty)
        technotype_list = Technotype.objects.filter(difficulty = difficulty)
    except Exception as e:
        logger.error(e)
    return render(request, 'list2.html', locals())

def needs(request):
    try:
        nid = request.GET.get('nid',None)
        did = request.GET.get('did',None) 
        try:
            need = Need.objects.get(pk=nid)
        except Need.DoesNotExist:
            return render(request, 'error.html', {"reason":"Besoin n'existe pas!"})
        difficulty = Difficulty.objects.get(pk=did)
        #technotype_list = Technotype.objects.filter(difficulty = difficulty)
        techno_list = Technology.objects.filter(need = need,difficulty = difficulty, show = True)
        technotype_list = []
        for techno in techno_list:
            each_list = Technotype.objects.filter(technology = techno)
            for each in each_list:
                if not each in technotype_list:
                    technotype_list.append(each)
        techno_list = getPage(request,techno_list) 
    except Exception as e:
        logger.error(e)
    return render(request, 'list2.html', locals())

def technotypes(request):
    try:
        typeid = request.GET.get('typeid',None)
        did = request.GET.get('did',None)
        try:
            technotype = Technotype.objects.get(pk=typeid)
        except Technotype.DoesNotExist:
            return render(request, 'error.html', {"reason":"Type de technologie n'existe pas!"})
        difficulty = Difficulty.objects.get(pk=did)
        techno_list = Technology.objects.filter(technotype = technotype, difficulty = difficulty, show = True)
        techno_list = getPage(request,techno_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'list2.html', locals())

def needs2types(request):
    
    typeid = request.GET.get('typeid',None)
    nid = request.GET.get('nid',None)
    did = request.GET.get('did',None) 
    
    need = Need.objects.get(pk=nid)
    technotype = Technotype.objects.get(pk=typeid)
    difficulty = Difficulty.objects.get(pk=did)
    
    techno_list = Technology.objects.filter(technotype = technotype,need = need,difficulty = difficulty, show = True)
    techno_list = getPage(request,techno_list)

    return render(request, 'list2.html', locals())
    

def search(request):    
    q = request.GET["q"].split(" ")
    techno_list = Utils.search_in_objects(q)
    n_results =  len(techno_list)
    return render(request, "list2.html", locals())


def detail(request):
    try:
        technoid = request.GET.get('technoid', None)
        try:
            techno = Technology.objects.get(pk=technoid)
        except Technology.DoesNotExist:
            return render(request, 'error.html', {"reason":"Technologie n'existe pas!"})
        diff_list = Difficulty.objects.filter(technology = techno)
        type_list = Technotype.objects.filter(technology = techno)
    except Exception as e:
        logger.error(e)
        
    if not techno.video:
        logger.debug("No video found for techno '{}', running youtube lookup...".format(techno.name))
        techno.video = Utils.get_technology_video(techno.name)
        techno.save(update_fields=['video'])
    return render(request, 'detail.html', locals())

def getPage(request,techno_list):
    paginator = Paginator(techno_list,8)
    try:
        page = int(request.GET.get('page',1))
        techno_list = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        techno_list = paginator.page(1)
    return techno_list

#######################################################################################
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request,'error.html',{'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request,'register.html',locals())

def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username,password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                else:
                    return render(request,'error.html',{'reason': 'un erreur est produit'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'error.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())

def subform(request):

    if request.method == "POST":

        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            return render(request, "subform.html", {'form': form, 'success': 1})

        else:
            return render(request, "subform.html", {'form': form, 'success': 0})

    else:

        form = SubmissionForm()

    return render(request, "subform.html", {'form': form, 'success': 0})


###########################################################################################3
def about(request):

    """
    about page
    """

    return render(request, "about.html")

def contact(request):

    """
    contact page
    """

    return render_to_response("contact.html")
############################################################################################
@authenticated_view
def view_cart(request):
    cart = request.session.get(request.user.id, None)
    return render(request, 'checkout.html', locals())

#add item to wish list
@authenticated_view
def add_cart(request):
    try:
        technoid = request.POST.get('techid',None)
        try:
            techno = Technology.objects.get(pk=technoid)
        except Technology.DoesNotExist:
            return render(request, 'error.html', {'reason':"Technologie n'existe pas!"})
        cart = request.session.get(request.user.id,None)
        if not cart:
            cart = Cart()
            cart.add(techno)
            request.session[request.user.id] = cart
        else:
            cart.add(techno)
            request.session[request.user.id] = cart
        length = len(cart.items)
    except Exception as e:
        logger.error(e)
    return render(request, 'checkout.html', locals())

#clean wish list
@authenticated_view
def cleanCart(request):
    cart = Cart()
    request.session[request.user.id] = cart
    return render(request, 'checkout.html', locals())

#@authenticated_view
#def clean_one_item(request, id):
#    item = None
#    try:
#     item = Technology.objects.get(pk=id)
#    except Technology.DoesNotExist:
#        pass
#    if item:
#        item.delete()
#    cart = request.session.get(request.user.id, None)
#    return render(request, 'checkout.html', {'cart':cart})

########################################################################################
class Utils:

    @staticmethod
    def search_in_objects(words):

        """
        search
        in techno's attributes
        (need to find a replacement)

        """

        techno_list = Technology.objects.filter(show = True)
        match = []

        for word in words:
            for techno in techno_list:
                attributes = Utils.get_techno_attributes(techno)
                for att in attributes:
                    if word.lower() in att:
                        if not techno in match and techno.show:
                            match.append(techno)
        return match

    @staticmethod
    def get_techno_attributes(techno):
        attributes = [i.lower() for i in techno.__dict__.values() if type(i) == str]
        attributes.append(techno.get_type().lower())  
        attributes.append(techno.get_need().lower())  
        return attributes

    @staticmethod
    def get_technology_video(name):

        """
        not so great method to get a video
        describing the techno from youtube
        """

        query_string = urllib.parse.urlencode({"search_query": name})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        return "http://www.youtube.com/embed/" + search_results[0]
