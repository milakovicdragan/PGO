from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from allauth.account.auth_backends import AuthenticationBackend
from django.utils import timezone
from django.contrib.auth import authenticate


class SessionLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Call the AuthenticationBackend to get the authenticated user
        auth_backend = AuthenticationBackend()
        #print(auth_backend)
        user = auth_backend.authenticate(request)

        #user = authenticate(request, username, password)

        # Check if the user is authenticated
        # print(request)
        # print(user)
        if user is not None:
            # Get the number of active sessions for the user
            session_count = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_key__in=user.session_keys
            ).count()

            # Check if the user has exceeded the session limit
            if session_count >= 1: # Example limit is 2 sessions per user
                # Delete all sessions except for the current one
                for session in Session.objects.filter(
                    expire_date__gte=timezone.now(),
                    session_key__in=user.session_keys
                ).exclude(session_key=request.session.session_key):
                    session.delete()

            # Set the authenticated user on the request object
            request.user = user

        # Call the next middleware or view
        response = self.get_response(request)

        return response
