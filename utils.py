import aiohttp, os

# Constants
server_token = os.environ.get("MILTON_SERVER_TOKEN")
server_url = os.environ.get("MILTON_SERVER_URL")

# HTTP request variables
webserver_session = aiohttp.ClientSession()
webserver_headers = {
    'Authorization': 'Token ' + server_token
}

# Milton API call methods

async def clip_get(params):
    """
    Performs GET request on /clips endpoint of Milton API

    Parameters:
    params (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    async with webserver_session.get(server_url + '/clips/',
                                    headers=webserver_headers,
                                    params=params) as resp:
        return await resp.json()

async def board_get(params):
    """
    Performs GET request on /boards endpoint of Milton API

    Parameters:
    params (dict): the request parameters

    Returns:
    str: json string of API call result
    """
    async with webserver_session.get(server_url + '/boards/',
                                    headers=webserver_headers,
                                    params=params) as resp:
        return await resp.json()
