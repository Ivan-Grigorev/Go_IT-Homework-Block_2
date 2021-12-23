import httpx
import redis


def get_api_info(name):
    with httpx.Client() as web_user:
        base_url = 'https://api.nationalize.io?name'
        url = f"{base_url}={name}"

        response = web_user.get(url)
        return response.json()['country'][0]['country_id']


def get_cache_info(name, user):
    value = user.get(name)
    return value


def set_cache_info(name, value, user):
    data = user.set(name, value)
    return data


def analyze_cache(name, user):
    data = get_cache_info(name, user)
    if data:
        print(f"{data.decode('UTF-8')} received from cache.")
    else:
        data = get_api_info(name)
        print(f"{data} received from API.")
        if data:
            state = set_cache_info(name=name, value=data, user=user)
            return state


if __name__ == '__main__':
    redis_user = redis.Redis(host='localhost', port=6380, db=0)

    analyze_cache('fred', redis_user)

