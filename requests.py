import utils

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
        server_json = await utils.clip_get(params={
            "clip": clip,
            "board": board
        })
        return next((entry['sound'] for entry in server_json), None)
    except Exception as e:
        print(e)
    