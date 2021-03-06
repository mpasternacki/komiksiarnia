import re

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from models import Seria, Pasek, User
from tagging.models import Tag, TaggedItem
import tagging.models

def redirect(m):
    return HttpResponseRedirect(m.get_absolute_url())

def wszystkie_serie(request, seria):
    return seria == '*'

def wybrane_serie(request,seria):
    return request.user.is_authenticated() and seria == '**'

def seria(request, seria):
    if wybrane_serie(request,seria):
        ign = request.user.get_profile().serie_ignorowane
        return render_to_response('komiksy/pasek_list_no_pagination.html',
                                  dict(object_list=[
                                      s.last
                                      for s in Seria.objects.all()
                                      if (not ign) or (s not in ign.all()) ],
                                       title='ostatnie paski wybranych serii'),
                                  context_instance=RequestContext(request))
    elif wszystkie_serie(request,seria):
        return render_to_response('komiksy/pasek_list_no_pagination.html',
                                  dict(object_list=[s.last for s in Seria.objects.all()],
                                       title='ostatnie paski wszystkich serii'),
                                  context_instance=RequestContext(request))
    s = get_object_or_404(Seria, tytul=seria)
    return redirect(s.last)

def random(request,seria):
    if seria == '*':
        qs = Pasek.objects.all()
    else:
        qs = Pasek.objects.filter(seria=get_object_or_404(Seria, tytul=seria))
    if request.user.is_authenticated():
        qs = qs.exclude(
            seria__in=request.user.get_profile().serie_ignorowane.all() )
    return redirect(qs.order_by('?')[0])

def tag_list(request, seria):
    if seria == '*':
        s = {'tytul':'*', 'pelny_tytul':'wszystkich serii'}
        if request.user.is_authenticated():
            tt = Tag.objects.usage_for_queryset(Pasek.objects.exclude(
                seria__in=request.user.get_profile().serie_ignorowane.all()),
                                             counts=True)
        else:
            tt = Tag.objects.usage_for_model(Pasek, counts=True)
    else:
        s = get_object_or_404(Seria, tytul=seria)
        tt = Tag.objects.usage_for_model(Pasek, filters=dict(seria=s), counts=True)
    tagging.models.calculate_cloud(tt)
    return render_to_response('komiksy/tag_list.html',
                              dict(seria=s, tagi=tt),
                              context_instance=RequestContext(request))

def tag(request, seria, tag):
    tag = Tag.objects.get(name=tag)
    if seria == '*':
        pp = TaggedItem.objects.get_by_model(Pasek, tag)
        t = 'paski wszystkich serii oznaczone tagiem ' + tag.name
    else:
        s = get_object_or_404(Seria, tytul=seria)
        pp = TaggedItem.objects.get_by_model(
            Pasek.objects.filter(seria=s), tag)
        t = 'paski z serii ' + s.pelny_tytul + ' oznaczone tagiem ' + tag.name
    return render_to_response('komiksy/pasek_list.html',
                              dict(object_list=pp, title=t),
                              context_instance=RequestContext(request))

def pasek(request, seria, namiar):
    s = get_object_or_404(Seria, tytul=seria)

    ext = None
    if namiar.find(',') >= 0: namiar, ext = namiar.split(',',1)

    p = None
    if re.match(r'^\d+$', namiar):
        p = get_object_or_404(Pasek, seria=s, numer=namiar, rozszerzenie=ext)
    else:
        p = get_object_or_404(Pasek, seria=s, data=namiar, rozszerzenie=ext)

    if request.method=='GET': return render_to_response(
        'komiksy/pasek_detail.html',
        {'pasek':p}, context_instance=RequestContext(request))

    if request.method=='POST':
        if request.POST['action'] == 'tag':
            Tag.objects.add_tag(p, '"%s"'%request.POST['tag'])
        return redirect(p)

def new_redirect(request, seria=None):
    mid = Pasek.max_id()

    if 'curr_max_id' in request.COOKIES:
        last_mid = int(request.COOKIES['curr_max_id'])
    else:
        if request.user.is_authenticated():
            p = request.user.get_profile()
            last_mid = p.max_id
            p.max_id = mid
            p.save()
        if 'max_id' in request.COOKIES:
            last_mid = int(request.COOKIES['max_id'])
        else:
            last_mid = mid

    if seria is None: url = '/new/%d/' % last_mid
    else: url = '/%s/new/%d/' % ( seria, last_mid )

    resp = HttpResponseRedirect(url)
    resp.set_cookie('current_max_id', str(last_mid), 3600)
    resp.set_cookie('max_id', str(mid), 60*60*24*6004)
    return resp

def new_simple(request, seria, maxid):
    maxid = int(maxid)
    if seria == '*':
        pp = Pasek.objects.filter(id__gt=maxid)
        if request.user.is_authenticated():
            pp = pp.exclude(seria__in=request.user.get_profile().serie_ignorowane.all())
        t = 'Nowe paski'
    else:
        s = get_object_or_404(Seria, tytul=seria)
        pp = Pasek.objects.filter(id__gt=maxid, seria=s)
        t = 'Nowe ' + s.pelny_tytul
    return render_to_response('komiksy/pasek_list.html',
                              dict(object_list=pp, title=t),
                              context_instance=RequestContext(request))

def new_complex(request, maxid):
    maxid = int(maxid)
    ss = Seria.objects.filter(last__gt=maxid)
    if request.user.is_authenticated():
        ign = set(request.user.get_profile().serie_ignorowane.all())
    else:
        ign=set([])
    pp = [s.last for s in ss if s not in ign]
    for p in pp:
        if p.seria.moar(maxid) > 1:
            p.moar = maxid

    return render_to_response('komiksy/pasek_list_no_pagination.html',
                              dict(object_list=pp,
                                   title='Nowe paski',
                                   maxid=maxid),
                              context_instance=RequestContext(request))
