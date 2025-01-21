from fastapi import Request


# Util function used by the db middleware
# Provides per-request sessions via FastAPI dependency. Expects that a session
# is attached to the request state which is normally done through the middleware
# mounted to apps.
def get_db(request: Request):
    return request.state.db
