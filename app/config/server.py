from pydantic.main import BaseModel


class Server_config(object):
    prefix = "/api/v1"
    responses = {404: {"description": "Not found"}}