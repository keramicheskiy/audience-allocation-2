from django.shortcuts import render
from frontend.settings import TG_BOT_LINK

# Create your views here.
def info(request):
    context = {"link": TG_BOT_LINK}
    return render(request, "tg_bot/info.html", context=context)
