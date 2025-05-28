from django.shortcuts import render, redirect

from apps.authentication.decorators import authenticated
from apps.authentication.utils import get_user


@authenticated()
def profile(request):
    user = get_user(request)
    return redirect(to='/users/{}')


    return render(request, "", context={"user": request.user})

@authenticated()
def user_profile(request):


