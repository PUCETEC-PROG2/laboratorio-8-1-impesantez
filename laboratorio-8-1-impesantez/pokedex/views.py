from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from .models import Pokemon
from .forms import PokemonForm

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    #pokemons = Pokemon.objects.all() 
    pokemons = Pokemon.objects.order_by('type')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'pokemons': pokemons}, request))

def pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request)) 

def add_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm() 
    return render(request, 'add_pokemon.html', {'form': form})   

class CustomLoginView(LoginView):
    template_name = "login.html"