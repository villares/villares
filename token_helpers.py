try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib # tomllib will be in Python 3.11's standard library only

def get_token(category, token):
    with open("/home/villares/api_tokens", "rb") as f:
        api_tokens = tomllib.load(f)
    return api_tokens[category][token]