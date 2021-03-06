import socket
import os
import json
from aiohttp.web import Response, Application, json_response, HTTPForbidden
import aiohttp_cors
from .lib.database import db_init
from .lib.utils import get_config, get_file, parse_auth_header
from .lib.loggers import logger
from .middleware.validation import validation
from .middleware.transaction import transaction
from .middleware.validate_app import validate_app
from .constants.ignore import ignore_validation


def create_app():
    file_name = get_file(path="config", extention="py")
    config, config_error = get_config(file_name=file_name)

    if config_error:
        raise config_error
   
    app = Application(middlewares=[
        validate_app,
        validation(ignore=ignore_validation),
        transaction
        ])

    app["config"] = config
    db_init(app)

    # apikey = config["HOSTEDGRAPHITE_APIKEY"]
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.sendto("%s.request.time 1444\n" % apikey, ("carbon.hostedgraphite.com", 2003))

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

    from .api.routes import (
        handle_authenticate_profile,
        handle_get_profile,
        handle_token_validation,
        handle_token_exchange,
        handle_add_eats,
        handle_search_eats,
        handle_browse_eats, 
        handle_get_eats)

    cors.add(app.router.add_post('/api/v1/profile', handle_authenticate_profile))
    cors.add(app.router.add_get('/api/v1/profile', handle_get_profile))
    cors.add(app.router.add_put('/api/v1/profile', handle_authenticate_profile))
    cors.add(app.router.add_get('/api/v1/exchange', handle_token_exchange))
    cors.add(app.router.add_get('/api/v1/validation', handle_token_validation))
    #eats 
    cors.add(app.router.add_get('/api/v1/eats', handle_get_eats))
    cors.add(app.router.add_post('/api/v1/eats', handle_add_eats))
    cors.add(app.router.add_get('/api/v1/eats/search', handle_search_eats))
    cors.add(app.router.add_get('/api/v1/eats/browse', handle_browse_eats))

    return app 