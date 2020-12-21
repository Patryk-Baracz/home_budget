from django.shortcuts import render
from django.views import View
from budget_app.models import FamilyMember
from django.shortcuts import redirect


# Create your views here.

def log_check(request):
    member_id = request.session.get('family_member_id', None)
    if not member_id:
        return redirect('/login')


class Index(View):
    def get(self, request):
        log_check(request)
        return render(request, 'index.html')

    def post(self, request):
        log_check(request)
        return render(request, 'index.html')


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
