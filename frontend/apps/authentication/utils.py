import requests

from frontend.settings import BACKEND_URL


def get_request_user(request):
    cookies = {'Token': request.COOKIES.get('Token')}
    response = requests.get(BACKEND_URL + '/my/profile', cookies=cookies)
    return response.json()
