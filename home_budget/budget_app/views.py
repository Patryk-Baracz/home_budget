from django.shortcuts import render
from django.views import View
from budget_app.models import FamilyMember, Category, MoneyTransfer
from django.shortcuts import redirect
import datetime


# Create your views here.

def log_check(request):
    member_id = request.session.get('family_member_id', None)
    if not member_id:
        return redirect('/login')


def index(request):
    maybe_redirect = log_check(request)
    if maybe_redirect:
        return maybe_redirect
    else:
        category = Category.objects.all()
        today = datetime.date.today
        return render(request, 'index.html', {'category': category, 'today': today})



class Login(View):
    def get(self, request):
        family_member = FamilyMember.objects.all()
        return render(request, 'login.html', {'family_member': family_member})

    def post(self, request):
        if request.POST['family_member'] == "new":
            if len(request.POST['new_family_member']) > 2:
                if not request.POST['new_family_member'] in FamilyMember.objects.all():
                    new_member = FamilyMember.objects.create(name=request.POST['new_family_member'])
                    request.session['family_member_id'] = new_member.id
                    return redirect('/')
                else:
                    pop = "Użytkownik o tym imieniu już istnieje!"
                    return (render(request, 'login.html', {'pop': pop}))
            else:
                pop = "Imię nowego użytkownika musi mieć więcej niż 2 znaki!"
                return (render(request, 'login.html', {'pop': pop}))
        else:
            request.session['family_member_id'] = request.POST['family_member']
            return redirect('/')

class Expense(View):
    def post(self, request):
        owner_id = request.session.get('family_member_id', None)
        owner = FamilyMember.objects.get(id=owner_id)
        description = request.POST['description']
        if request.POST['date']:
            day = request.POST['date']
        else:
            day = None
        amount = 0 - int(request.POST['amount'])
        category_id = request.POST['category']
        if category_id:
            category = Category.objects.get(id=category_id)
        else:
            category = None
        MoneyTransfer.objects.create(owner=owner, description=description, date=day, amount=amount, category=category)
        return redirect('/')

class Income(View):
    def post(self, request):
        owner_id = request.session.get('family_member_id', None)
        owner = FamilyMember.objects.get(id=owner_id)
        description = 'Wpływ do budżetu'
        if request.POST['date']:
            day = request.POST['date']
        else:
            day = None
        amount = int(request.POST['amount'])
        category = None
        MoneyTransfer.objects.create(owner=owner, description=description, date=day, amount=amount, category=category)
        return redirect('/')