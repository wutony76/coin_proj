from __future__ import print_function
from django.http import HttpResponseRedirect
from django.urls import reverse as reverse_url
#from django.core.urlresolvers import reverse as reverse_url




def past_get_request(fn):
  def inner(request, *args, **kwargs):
    print("inner", request)

    if request.method == 'GET':
      redirect_to = reverse_url("cash_list")
      return HttpResponseRedirect(redirect_to)

    return fn(request, *args, **kwargs)
  return inner





def print_ak_log(fn):
  def inner(request, *args, **kwargs):
    print("inner", request)

    print( "ak_log--%s--%s--%s"%(request.META["REMOTE_ADDR"], request.META["HTTP_USER_AGENT"], request.META["PATH_INFO"]))

    #values = request.META.items()
    #values.sort()
    #for k, v in values:
    #  print( k, " - ", v)

    return fn(request, *args, **kwargs)
  return inner



def login_required(fn):
  def inner(request, *args, **kwargs):
    try:
      req_tag = request.GET["tag"]
    except:
      req_tag = None

    #print("login_required")
    #print("login_required req_tag" , req_tag)
    #print("+" * 100)
    #print("login_required", request, request.COOKIES)
    if not request.user.is_authenticated():
      if req_tag is not None:
        if req_tag == "drawgame":
          redirect_to = reverse_url("web_login") + "?redirect=https://www.acekinggames.com/girls_games?tag=drawgame"
        else:
          redirect_to = reverse_url("web_login")
      else: 
        redirect_to = reverse_url("web_login")

      #redirect_to = reverse_url("web_index")
      return HttpResponseRedirect(redirect_to)

    #if req_tag == "drawgame":
    #  return HttpResponseRedirect(reverse_url("web_girls_games") + "?tag=drawgame" ) 


    return fn(request, *args, **kwargs)
  return inner


def store_login_required(fn):
  def inner(request, *args, **kwargs):
    #print("redirect_login_required")
    #print("+" * 100)
    #print("login_required", request, request.COOKIES)
    if not request.user.is_authenticated():
      redirect_to = reverse_url("web_login")+"?redirect=https://store.acekinggames.com"
      #redirect_to = reverse_url("web_index")
      return HttpResponseRedirect(redirect_to)
    return fn(request, *args, **kwargs)
  return inner


def store_product_login_required(fn):
  def inner(request, *args, **kwargs):
    #print("redirect_login_required")
    #print("+" * 100)
    #print("login_required", request, request.COOKIES)
    if not request.user.is_authenticated():
      redirect_to = reverse_url("web_login")+"?redirect=https://store.acekinggames.com/akproduct/index"
      #redirect_to = reverse_url("web_login")+"?redirect=https://www.wangzugames.com:444/akproduct/index"
      #https://www.wangzugames.com:444/akproduct/index
      #redirect_to = reverse_url("web_index")
      return HttpResponseRedirect(redirect_to)
    return fn(request, *args, **kwargs)
  return inner
