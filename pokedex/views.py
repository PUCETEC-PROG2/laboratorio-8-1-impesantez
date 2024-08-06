from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from .models import Pokemon, Trainer
from .forms import PokemonForm, TrainerForm

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    #pokemons = Pokemon.objects.all() 
    pokemons = Pokemon.objects.order_by('type')
    trainers = Trainer.objects.order_by('level')
    template = loader.get_template('index.html')
    context = {
        'pokemons': pokemons,
        'trainers': trainers,    
        }
    return HttpResponse(template.render(context, request))

def pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon,
        }
    return HttpResponse(template.render(context, request))

def trainer(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    template = loader.get_template('display_trainer.html')
    context = {
        'trainer': trainer,    
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
    return render(request, 'pokemon_form.html', {'form': form}) 


def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = TrainerForm()
    
    return render(request, 'trainer_form.html', {'form': form})   

@login_required
def edit_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, pk = id)
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm(instance=pokemon) 
        
    return render(request, 'pokemon_form.html', {'form': form})  

@login_required
def edit_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk = id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = TrainerForm(instance=trainer)
    
    return render(request, 'trainer_form.html', {'form': form})

@login_required
def delete_pokemon(request, id):
     pokemon = get_object_or_404(Pokemon, pk = id)
     pokemon.delete()
     return redirect('pokedex:index')

@login_required
def delete_trainer(required, id):
    trainer = get_object_or_404(Trainer, pk = id)
    trainer.delete()
    return redirect('pokedex:index')

class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLoginView(LoginView):
    template_name = "login.html"