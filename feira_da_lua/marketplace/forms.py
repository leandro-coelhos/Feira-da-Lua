from django import forms
from .models import MarketPlace, Products

class SearchForm(forms.Form):
    SEARCH_TYPE_CHOICES = [
        ('feiras', 'Feiras'),
        ('produtos', 'Produtos'),
    ]
    
    query = forms.CharField(
        max_length=255,
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Buscar feiras ou produtos...'
        })
    )
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPE_CHOICES,
        required=False,
        initial='feiras',
        label='Tipo',
        widget=forms.RadioSelect(attrs={
            'class': 'search-type-radio'
        })
    )


class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Preco Minimo',
        widget=forms.NumberInput(attrs={
            'class': 'form-input filter-input',
            'placeholder': '0,00',
            'step': '0.01',
            'min': '0'
        })
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Preco Maximo',
        widget=forms.NumberInput(attrs={
            'class': 'form-input filter-input',
            'placeholder': '1000,00',
            'step': '0.01',
            'min': '0'
        })
    )


class MarketPlaceFilterForm(forms.Form):
    FILTER_CHOICES = [
        ('', 'Todos'),
        ('rating', 'Melhor Avaliados'),
        ('location', 'Por Localizacao'),
        ('nearby', 'Proximos a Mim'),
    ]
    
    RATING_CHOICES = [
        ('', 'Todas as Notas'),
        ('4', '4 estrelas ou mais'),
        ('3', '3 estrelas ou mais'),
        ('2', '2 estrelas ou mais'),
    ]
    
    filter_type = forms.ChoiceField(
        choices=FILTER_CHOICES,
        required=False,
        label='Filtrar por',
        widget=forms.Select(attrs={
            'class': 'form-input filter-select'
        })
    )
    min_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        required=False,
        label='Nota Minima',
        widget=forms.Select(attrs={
            'class': 'form-input filter-select'
        })
    )
    location = forms.CharField(
        max_length=255,
        required=False,
        label='Cidade/Bairro',
        widget=forms.TextInput(attrs={
            'class': 'form-input filter-input',
            'placeholder': 'Digite a localizacao...'
        })
    )
    user_lat = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'user-lat'})
    )
    user_lon = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'user-lon'})
    )
    max_distance = forms.IntegerField(
        required=False,
        initial=10,
        label='Distancia Maxima (km)',
        widget=forms.NumberInput(attrs={
            'class': 'form-input filter-input',
            'placeholder': '10',
            'min': '1',
            'max': '100'
        })
    )





class MarketPlaceForm(forms.ModelForm):
    class Meta:
        model = MarketPlace
        fields = ['name', 'address', 'coordinates']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'coordinates': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ProductForm(forms.ModelForm):
    photo = forms.FileField(
        required=False,
        label='Foto do Produto',
        widget=forms.FileInput(attrs={'class': 'form-input'})
    )
    
    class Meta:
        model = Products
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
        }
