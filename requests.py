import utils
import logging

if (os.environ.get("LOGGING_MODE") == 'file'):
    logging.basicConfig(filename='milton.log',level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# REST request methods
#
# These methods are written to be called on the milton API, whose data format of return values 
# can be found in the documentation in the milton webserver repository, at https://github.com/redwallguy/milton-web-server.git

async def get_clip(clip, board):
    """
    Performs a GET request on the /clips endpoint on the webserver with the specified
    clip and board query params to find clip, then requests presigned URL for playback.

    If the clip cannot be found, it performs a GET request on the /aliases endpoint of 
    the webserver to search for an alias on the specified board, and uses the associated 
    clip to request presigned URL for playback.

    Parameters:
        clip (str): Name of clip
        board (str): Name of board

    Returns:
        str: URL of clip audio
    """
    clip_id = None
    volume = None
    try:
        server_json = await utils.clip_get(params={
            "name": clip,
            "board": board
        })
        logger.info(server_json)
        clip_id, volume = next(((str(entry['id']), int(entry['volume'])) for entry in server_json), (None, None))
    except Exception as e:
        logger.info("Error in get_clip " + e)
    if (clip_id is None):
        logger.info("trying aliases")
        try:
            alias_server_json = await utils.alias_clip_get(params={
                "name": clip,
                "board": board
            })
            logger.info(alias_server_json)
            clip_id, volume = str(alias_server_json['id']), int(alias_server_json['volume'])
        except Exception as e:
            logger.info("Error in alias_clip_get " + e)
    if (clip_id is not None and volume is not None):
        logger.info("Getting presigned url")
        presigned_url = await utils.clip_url_get(key=clip_id)
        logger.info(repr(presigned_url))
        return presigned_url, volume
    else:
        raise utils.ClipNotFoundException("Error generating presigned URL")

async def list_board(board):
    """
    Performs GET request on /clips endpoint of the webserver with specified board 
    param to find all clips on that board.

    Then performs GET request on /aliases endpoint of the webserver with specified 
    board param to find all aliases on that board.

    Returns a list of clip objects of the form {"name": name, "aliases": [a1, a2,...]}

    Parameters:
        board (str): Name of board

    Returns:
        List[clips]: Clips of board
    """
    board_list = []
    alias_list = []
    try: # Get the clips on the board
        board_list = await utils.clip_get(params={
            "board": board
        })
        logger.info(board_list)
    except Exception as e:
        logger.info("Error in clip_get " + e)
    try: # Get the aliases on the board
        alias_list = await utils.alias_from_board_get(params={  # Get aliases in one request to reduce overhead of requests for each clip
            "name": board
        })
        logger.info(alias_list)
    except Exception as e:
        logger.info("Error in alias_from_board_get " + e)
    try: # Merge clip and alias information, then trim unnecessary information
        temp_list = []
        for clip in board_list:
            clip_object = {
                "name": clip["name"],
                "aliases": [a["name"] for a in alias_list if a["clip"]["id"] == clip["id"]],
                "volume": clip["volume"]
            }
            temp_list.append(clip_object)
        board_list = temp_list
    except Exception as e:
        logger.info("Error in clip/alias merge " + e)
    return board_list
    