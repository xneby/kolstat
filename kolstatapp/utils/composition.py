from kolstatapp.models import Composition
from kolstatapp.exceptions import KolstatError

VALID_CARS = [
    'EU07', 'EP07', 'EP08', 'EP09', 'SM42', 'ET22',
    'Admnu', 'Adnu',
    'Bdhpumn', 'Bdmnu', 'Bdnu', 'Bc', 'BDdsu',
    'EN57', 'ED72', 'ED74', 'EN75', 'EN94', 'EN95',
    'SA110', 'SA131', 'SA134',
    'ABdnu', 'WLAB', 'WRbd'
            ]

def parse_composition(comp):
    if comp == '': return None
    
    cars = comp.split('+')
    for car in cars:
        if car not in VALID_CARS:
            raise KolstatError('Bad request')
        
    try:
        return Composition.objects.get(composition = comp)
    except Composition.DoesNotExist:
        return Composition(composition = comp)