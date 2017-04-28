from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http import Http404
from invitations.models import Invitation
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import ItemForm, ListForm, InviteForm
from .models import Item, List, Invites



# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('tobuy:login'))
    user = request.user
    user_lists = List.objects.filter(users=user)
    active_list = user.profile.active_list

    form = ItemForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.items_list = active_list
        instance.save()
        return redirect('tobuy:home')

    active = Item.objects.filter(active=True, items_list=active_list)
    inactive = Item.objects.filter(active=False, items_list=active_list)
    context = { 'active': active,
                'inactive': inactive,
                'form': form,
                'user_lists': user_lists,
                'active_list': active_list,}
    return render(request, 'tobuy/home.html', context)

def switch(request, pk=None):
    item = Item.objects.get(pk=pk)
    item.active = False
    item.save()
    user = request.user
    active_list = user.profile.active_list
    inactive = Item.objects.filter(active=False, items_list=active_list)
    return render(request, 'tobuy/only_inactive.html', {'inactive': inactive})

def only_active(request):
    user = request.user
    active_list = user.profile.active_list
    active = Item.objects.filter(active=True, items_list=active_list)
    return render(request, 'tobuy/only_active.html', {'active': active})

def switch2(request, pk=None):
    item = Item.objects.get(pk=pk)
    item.active = True
    item.save()
    user = request.user
    active_list = user.profile.active_list
    active = Item.objects.filter(active=True, items_list=active_list)
    return render(request, 'tobuy/only_active.html', {'active': active})

def only_inactive(request):
    user = request.user
    active_list = user.profile.active_list
    inactive = Item.objects.filter(active=False, items_list=active_list)
    return render(request, 'tobuy/only_inactive.html', {'inactive': inactive})

def additem(request):
    if not request.user.is_staff:
        raise Http404
    form = ItemForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        first_list = List.objects.get(name='testlist')
        instance.items_list = first_list
        instance.save()

def change_active_list(request, pk):
    user = request.user
    user.profile.active_list = List.objects.get(pk=pk)
    user.profile.save()
    return redirect('tobuy:home')

def add_new_list(request):
    form = ListForm(request.POST or None)
    if form.is_valid():
        user = request.user
        instance = form.save()
        instance.users.add(user)
        instance.save()
       
        user.profile.active_list = instance
        user.profile.save()
        return redirect('tobuy:home')
    return render(request, 'tobuy/add_new_list.html', {'form': form})

def invite_user(request):
    invite_form = InviteForm(request.POST or None)
    if invite_form.is_valid():
        email = invite_form.cleaned_data['email']
        # if email belongs to a registered user:
        if User.objects.filter(email=email).exists():
            print(User.objects.filter(email=email))
        #     add list to user
        #     send him a message about new list

        else:
        # if email belongs to a prospective user send email to invite, associate email with list:
            user = request.user
            list_to_invite = user.profile.active_list
            invite_store = Invites(email=email, list_to_invite=list_to_invite, sender=user)
            invite_store.save()
            invite_email = Invitation.create(email, inviter=user)
            invite_email.send_invitation(request)

        # success message
        messages.success(request, "Invitation to share this list has been sent")
        return redirect('tobuy:home')
    return render(request, 'tobuy/invite_user.html', {'invite_form': invite_form})
        