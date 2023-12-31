import datetime
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from login.models import User, Affinity
import uuid
from .forms import ProductForm

def create_product(request):
    user_id = request.session.get('user_id')
    print(user_id)
    if not user_id:
        return redirect('login')  
    user = User.objects.get(user_id=user_id)
    print(user)
    form = ProductForm(request.POST, request.FILES or None)
    print(request.POST)
    if form.is_valid():
        product = form.save(commit=False)
        product.prod_id = uuid.uuid4().hex
        product.prod_seller = user
        product.prod_date = datetime.date.today().isoformat()
        product.prod_active = True
        affinitie1_id = form.cleaned_data["prod_affinitie1"]
        affinitie2_id = form.cleaned_data["prod_affinitie2"]
        
        affinitie1 = Affinity.objects.get(pk=affinitie1_id)
        affinitie2 = Affinity.objects.get(pk=affinitie2_id)
        
        product.prod_affinitie1 = affinitie1.af_id
        product.prod_affinitie2 = affinitie2.af_id
        product.save()
        return redirect('home')
    context = {'form': form, 'hide_footer': True}
    return render(request, 'create_product.html', context)
