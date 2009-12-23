from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from komiksiarnia.komiksy.models import Seria

from django import forms
class ProfileForm(forms.Form):
    serie = forms.MultipleChoiceField(
        label = u'Ukryj serie',
        widget = forms.CheckboxSelectMultiple,
        choices = [(s.id, s.pelny_tytul) for s in Seria.objects.all()],
        required=False
        )

@login_required
def user_profile(request):
    if request.method == 'POST':
        serie_form = ProfileForm(request.POST)
        if serie_form.is_valid():
            request.user.get_profile().serie_ignorowane = Seria.objects.filter(
                id__in=[int(sid) for sid in serie_form.cleaned_data['serie']] )
    else:
        serie_form = ProfileForm(
            dict(serie=[s.id for s in request.user.get_profile().serie_ignorowane.all()]) )

    passwd_form = PasswordChangeForm({})

    return render_to_response('registration/profile.html',
                              dict(serie_form=serie_form, passwd_form=passwd_form),
                              context_instance=RequestContext(request))

def createuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password1'])
            u.save()

            p = UserProfile(
                user = u,
                max_id = Pasek.max_id())
            p.save()

            # a call to authenticate() is needed.
            login(request,authenticate(username=form.cleaned_data['username'],
                                       password=form.cleaned_data['password1']))
            return HttpResponseRedirect(reverse('komiksiarnia.lusers.views.user_profile'))
    else:
        form = UserCreationForm()
    return render_to_response('registration/createuser.html',
                              dict(form=form),
                              context_instance=RequestContext(request))
