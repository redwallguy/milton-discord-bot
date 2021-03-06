import aiohttp, os, logging

if (os.environ.get("LOGGING_MODE") == 'file'):
    logging.basicConfig(filename='milton.log',level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Constants
server_username = os.environ.get("MILTON_SERVER_USERNAME")
server_password = os.environ.get("MILTON_SERVER_PASSWORD")
server_token = ""
server_url = os.environ.get("MILTON_SERVER_URL")

# HTTP request variables
webserver_session = aiohttp.ClientSession()
webserver_headers = {
    'Authorization': 'Token ' + server_token
}

# Milton API call methods

async def generate_token():
    """
    Performs POST request on /api-token-auth endpoint of Milton API to generate a token

    Parameters:

    Returns:
    token (str): Milton webserver token
    """
    async with webserver_session.post(server_url + '/api-token-auth/',
                                    data={
                                        'username': server_username,
                                        'password': server_password
                                    }) as resp:
        json = await resp.json()
        token = json.get("token")
        webserver_headers['Authorization'] = 'Token ' + token

async def _get(path, params={}):
    """
    Helper method for making a GET request to a Milton url. Adds webserver token header 
    and regenerates token if invalid.

    Parameters:
    path (str): path for GET request
    params (dict): parameters for GET request

    Returns:
    str: json string of API call result
    """
    async with webserver_session.get(server_url + "/api" + path,
                                    headers=webserver_headers,
                                    params=params) as resp:
        if (resp.status == 200):
            return await resp.json()
        elif (resp.status == 401):
            await generate_token()
            return "Token required regeneration. Please retry."
        else:
            return "Response error: " + resp.status

async def _post(path, data):
    """
    Helper method for making a POST request to a Milton url. Adds webserver token header 
    and regenerates token if invalid.

    Parameters:
    path (str): path for POST request
    data (dict): parameters for POST request

    Returns:
    str: json string of API call result
    """
    async with webserver_session.post(server_url + "/api" + path,
                                        headers=webserver_headers,
                                        json=data) as resp:
        if (resp.status == 200):
            return await resp.json()
        elif (resp.status == 401):
            await generate_token()
            return "Token required regeneration. Please retry."
        else:
            return "Response error " + str(resp.status)

async def _patch(path, data):
    """
    Helper method for making a PATCH request to a Milton url. Adds webserver token header 
    and regenerates token if invalid.

    Parameters:
    path (str): path for PATCH request
    data (dict): parameters for PATCH request

    Returns:
    str: json string of API call result
    """
    async with webserver_session.patch(server_url + "/api" + path,
                                        headers=webserver_headers,
                                        json=data) as resp:
        if (resp.status == 200):
            return await resp.json()
        elif (resp.status == 401):
            await generate_token()
            return "Token required regeneration. Please retry."
        else:
            return "Response error: " + str(resp.status)

async def clip_get(params):
    """
    Performs GET request on /clips endpoint of Milton API

    Parameters:
    params (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    return await _get('/clips/', params)

async def alias_clip_get(params):
    """
    Performs GET request on /aliases/get_clip endpoint of Milton API

    Parameters:
    params (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    return await _get('/aliases/get_clip/', params)

async def alias_from_board_get(params):
    """
    Performs GET request on /aliases/get_from_board endpoint of Milton API

    Parameters:
    params (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    return await _get('/aliases/get_from_board/', params)

async def clip_url_get(key):
    """
    Performs GET request on /clips/<key>/get_presigned_url endpoint of Milton API

    Parameters:
    key (int): the clip key

    Returns:
    str: json string of API call result
    """
    return await _get('/clips/' + key + '/get_presigned_url/')

async def board_get(params):
    """
    Performs GET request on /boards endpoint of Milton API

    Parameters:
    params (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    return await _get('/boards/', params)

async def user_get(params):
    """
    Performs GET request on /discord-users endpoint of Milton API

    Parameters:
    params (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    return await _get('/discord-users/', params)

async def user_post(data):
    """
    Performs POST request on /discord-users endpoint of Milton API

    Parameters:
    data (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    return await _post('/discord-users/', data)

async def user_patch(data, user_id):
    """
    Performs PATCH request on /discord-users/<user_id> endpoint of Milton API.
    Updates instance <user-id> with provided data.

    Parameters:
    data (dict): the request parameters
    user_id (str): id of the discord user instance

    Returns:
    str: json string of API call result
    """
    logger.info("disc user patch data: " + str(data))
    return await _patch('/discord-users/' + str(user_id) + "/", data)

# Exceptions
class ClipNotFoundException(Exception):
    pass
