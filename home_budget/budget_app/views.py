from django.shortcuts import render
from django.views import View
from budget_app.models import FamilyMember, Category, MoneyTransfer
from django.shortcuts import redirect
import datetime
import calendar
from django.http import JsonResponse

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
        today = str(datetime.date.today())
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


def date_to_int(date):
    d = date.split('-')
    return datetime.date(int(d[0]), int(d[1]), int(d[2]))


class Expense(View):
    def post(self, request):
        owner_id = request.session.get('family_member_id', None)
        owner = FamilyMember.objects.get(id=owner_id)
        description = request.POST['description']
        if request.POST['date']:
            day = date_to_int(request.POST['date'])
        else:
            day = datetime.date.today()
        amount = 0 - float(request.POST['amount'])
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
            day = date_to_int(request.POST['date'])
        else:
            day = datetime.date.today()
        amount = int(request.POST['amount'])
        category = None
        MoneyTransfer.objects.create(owner=owner, description=description, date=day, amount=amount, category=category)
        return redirect('/')


class Raport(View):
    def get(self, request):
        category = Category.objects.all()
        today = datetime.date.today()
        start = str(datetime.date(today.year, today.month, 1))
        last_day = calendar.monthrange(today.year, today.month)
        end = str(datetime.date(today.year, today.month, last_day[1]))
        family_member = FamilyMember.objects.all()
        return render(request, 'raport.html',
                      {'category': category, 'start': start, 'end': end, 'family_member': family_member})

    def post(self, request):
        transactions = MoneyTransfer.objects.all()
        q = request.POST['q']
        if q:
            transactions = transactions.filter(description__icontains=q)
        start = request.POST['start']
        if start:
            transactions = transactions.filter(date__gte=start)
        end = request.POST['end']
        if end:
            transactions = transactions.filter(date__lte=end)
        categories = request.POST.getlist('category')
        if categories:
            transactions = transactions.filter(category__id__in=categories)
        members = request.POST.getlist('family_member')
        if members:
            transactions = transactions.filter(owner__id__in=members)
        min = request.POST['min']
        if min:
            if min != '0':
                transactions = transactions.filter(amount__lte=f'-{min}')
        max = request.POST['max']
        if max:
            if max != '0':
                transactions = transactions.filter(amount__gte=f'-{max}')
        value = 0
        for trans in transactions:
            value += trans.amount
            if trans.category:
                trans.category.color = Category.objects.get(name=trans.category).color
            return render(request, 'raport-post.html', {'transactions': transactions, 'value': value})

class Hint(View):
    def get(self, request):
        text = request.GET.get('text')
        transactions = MoneyTransfer.objects.all()
        transactions = transactions.filter(description__icontains=text).values('description')
        trans_list = []
        for el in transactions:
            trans_list.append(el['description'])
        response = JsonResponse({'hints': trans_list})
        return response