import aiohttp
import os

# Environment variables
server_token = os.environ.get("MILTON_SERVER_TOKEN")
server_url = os.environ.get("MILTON_SERVER_URL")

# Common request constants
header_dict = {
    'Authorization': 'Token ' + server_token
}

# Request session initialization
webserver_session = aiohttp.ClientSession()

# REST request methods
#
# These methods are written to be called on the milton API, whose data format of return values 
# can be found in the documentation in the milton webserver repository, at https://github.com/redwallguy/milton-web-server.git

async def get_clip(clip, board):
    """
    Performs a GET request on the /clips endpoint on the webserver with the specified
    clip and board query params

    Arguments:
        clip: Name of clip (string)
        board: Name of board (string)

    Returns:
        URL of clip audio
    """
    try:
        async with webserver_session.get(server_url + '/clips',
                                headers=header_dict,
                                params={
                                    'board': board,
                                    'name': clip
                                }) as resp:
            server_json = await resp.json()
            return next((entry['sound'] for entry in server_json), None)
    except Exception as e:
        print(e)
    