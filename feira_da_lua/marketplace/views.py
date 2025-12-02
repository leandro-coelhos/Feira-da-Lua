from django.shortcuts import render
from .service import GetAllMarketplaces
# Create your views here.

def marketplace_home(request):
    marketplaces = GetAllMarketplaces()
    return render(request, 'marketplace/home.html', {'marketplaces': marketplaces})

def marketplace_detail(request, marketplace_id):
    # Placeholder for marketplace detail view
    return render(request, 'marketplace/detail.html', {'marketplace_id': marketplace_id})