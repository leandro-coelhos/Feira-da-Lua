from django.shortcuts import redirect
from .models import SiteAccess, User


class AuthRequiredMiddleware:
    EXEMPT_URLS = [
        '/login/',
        '/registro/',
        '/register/',
        '/register/feirante/',
        '/admin/',
        '/static/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not self._is_exempt(request.path):
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect('login')
            try:
                request.user_obj = User.objects.get(id=user_id)
            except User.DoesNotExist:
                del request.session['user_id']
                return redirect('login')
        else:
            request.user_obj = None
        
        return self.get_response(request)
    
    def _is_exempt(self, path):
        for url in self.EXEMPT_URLS:
            if path.startswith(url):
                return True
        return False


class SiteAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            user_agent = request.META.get('HTTP_USER_AGENT', '')
            session_key = request.session.session_key if hasattr(request, 'session') and request.session.session_key else None

            SiteAccess.objects.create(
                ip_address=ip_address,
                user_agent=user_agent,
                path=request.path,
                method=request.method,
                session_key=session_key
            )

        return response
