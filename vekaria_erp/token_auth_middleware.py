import json
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from channels.exceptions import StopConsumer

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        
        if token:
            user, error = await get_user_from_token(token[0])
            if error:
                await send({
                    "type": "websocket.accept"
                })
                await send({
                    "type": "websocket.send",
                    "text": json.dumps({"error": str(error)})
                })
                await send({
                    "type": "websocket.close"
                })
                return
            else:
                scope["user"] = user
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)


@database_sync_to_async
def get_user_from_token(token):
    try:
        auth = JWTAuthentication()
        # print("valid",token)
        validated_token = auth.get_validated_token(token)
        return auth.get_user(validated_token), None
    except AuthenticationFailed as e:
        print(e)
        return None, e.detail

