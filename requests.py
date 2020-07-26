import utils
import logging

logging.basicConfig(filename='milton.log',level=logging.INFO)
logger = logging.getLogger(__name__)

# REST request methods
#
# These methods are written to be called on the milton API, whose data format of return values 
# can be found in the documentation in the milton webserver repository, at https://github.com/redwallguy/milton-web-server.git

async def get_clip(clip, board):
    """
    Performs a GET request on the /clips endpoint on the webserver with the specified
    clip and board query params to find clip, then requests presigned URL for playback.

    Arguments:
        clip: Name of clip (string)
        board: Name of board (string)

    Returns:
        URL of clip audio
    """
    clip_id = None
    try:
        server_json = await utils.clip_get(params={
            "name": clip,
            "board": board
        })
        logger.info(server_json)
        clip_id = str(next((entry['id'] for entry in server_json), None))
    except Exception as e:
        logger.info("Error in get_clip " + e)
    if (clip_id != None):
        logger.info("Getting presigned url")
        presigned_url = await utils.clip_url_get(key=clip_id)
        logger.info(repr(presigned_url))
        return presigned_url
    else:
        raise utils.ClipNotFoundException("Error generating presigned URL")
    
    