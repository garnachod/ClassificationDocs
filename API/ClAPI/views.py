from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Train.ModelsLoader import ModelsLoader
from DBWrapper.I3Queries import I3Queries
from django.core.cache import cache

# TODO: MEMCACHE TIME SETINGS
MAXLENIDSOLR = 256
# Create your views here.
def index(request):
    return HttpResponse("You're at the API index.")

def classifyText(request):
    if request.method == 'GET':
        collection = None
        #url = host/classify_text?id=
        ###captura de los parametros de entrada, filtro
        # TODO: Seguridad
        if "id" in request.GET:
            id = request.GET['id']
            if len(id) > MAXLENIDSOLR:
                return _error(1)
            if "collection" in request.GET:
                collection = request.GET["collection"]

            return _doClassification(id, collection)
        else:
            return _error(1)

# AUXILIAR METHODS
def _doClassification(id, collection):
    q = I3Queries()
    text, lang = q.getTextSolr(id, collection=collection)
    if text == "err" or lang == "err":
        return _error(1)
    #memory
    m = cache.get("models")
    if m is None:
        m = ModelsLoader()
        cache.set("models", ModelsLoader(), 100)
        #print "setting"

    prediction = m[lang].predict(text)

    #print prediction
    return JsonResponse({'status': 'ok', 'prediction':prediction})

def _error(code):
    """

    :param code: 1 fallo en los parametros de entrada, 2 modelo no encontrado, 3 otro fallo
    :return: JSONRESPONSE
    """
    return JsonResponse({'status': 'error', 'code': code})