"""
Queste api devono simulare il comportamento di un servizio smart mensa che fornisce i
dati su quante persone sono in fila e i posti liberi in una mensa.

La velocità della fila è fissa per ogni mensa, si suppone calcolata a priori tramite dati storici,
ed è salvata in Mensa.queue_speed.

I posti delle mense sono gestiti in blocchi da 10 tavoli da 4 persone.
Ogni mensa ha un multiplo di questi blocchi.
Il numero di blocchi è salvato in Mensa.block_nbr

Essendo dati il cui storico non ci interessa, verranno salvati in dizionario.
"""

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from apps.mensa.models import Mensa

from .utils import init_mensa_data, update_mensa_data

mense_data = {}
"""
Mense data sample:

mensa_name: {
    queue_len: int, # people in queue
    wait_time: int, # estimated wait time in minutes
    timestamp: int, # last update timestamp
    block_list: [ # list of matrix blocks
        bit matrix, # 0 if free, 1 if occupied
    ],
    free_tables: int, # number of free tables
}
"""

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from apps.mensa.models import Mensa

from .utils import init_mensa_data, update_mensa_data

mense_data = {}


@cache_page(1)  # Cache the response for 1 second
def get_mensa_data(request, *args, **kwargs):
    name = kwargs.get('name')  # fix for name with spaces
    mensa = get_object_or_404(Mensa, name=name)

    if name not in mense_data.keys():
        mense_data[name] = init_mensa_data(mensa)
    else:
        mense_data[name] = update_mensa_data(mensa, mense_data[name])

    state = mense_data[name].copy()
    state['block_list'] = [block.tolist() for block in state['block_list']]
    return JsonResponse(state)
