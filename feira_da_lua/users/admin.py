from django.contrib import admin
from django.db.models import Count
from .models import User, Marketer, Avaliation, SiteAccess, SearchHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'complete_name')
    search_fields = ('username', 'email', 'complete_name')


@admin.register(Marketer)
class MarketerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'cellphone')
    search_fields = ('user__username', 'user__email')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Avaliation)
class AvaliationAdmin(admin.ModelAdmin):
    list_display = ('user', 'marketplace', 'grade', 'comment')
    list_filter = ('grade', 'marketplace')
    search_fields = ('user__username', 'comment')


@admin.register(SiteAccess)
class SiteAccessAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'method', 'timestamp', 'user_agent_short')
    list_filter = ('method', 'timestamp')
    search_fields = ('ip_address', 'path', 'user_agent')
    date_hierarchy = 'timestamp'
    readonly_fields = ('ip_address', 'user_agent', 'path', 'method', 'timestamp', 'session_key')

    def user_agent_short(self, obj):
        if len(obj.user_agent) > 50:
            return obj.user_agent[:50] + '...'
        return obj.user_agent
    user_agent_short.short_description = 'User Agent'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unique_visitors'] = SiteAccess.get_unique_visitors_count()
        extra_context['total_page_views'] = SiteAccess.get_total_page_views()
        
        top_pages = SiteAccess.objects.values('path').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        extra_context['top_pages'] = top_pages
        
        marketplace_visits = SiteAccess.get_marketplace_visits()
        extra_context['marketplace_visits'] = marketplace_visits
        
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('search_query', 'search_type', 'get_user_info', 'results_count', 'timestamp')
    list_filter = ('search_type', 'timestamp')
    search_fields = ('search_query', 'user__username', 'ip_address')
    date_hierarchy = 'timestamp'
    readonly_fields = ('user', 'ip_address', 'session_key', 'search_query', 'search_type', 'results_count', 'timestamp')

    def get_user_info(self, obj):
        if obj.user:
            return obj.user.username
        return obj.ip_address or 'Anonimo'
    get_user_info.short_description = 'Usuario/IP'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_searches'] = SearchHistory.get_total_searches()
        extra_context['unique_searchers'] = SearchHistory.get_unique_searchers()
        extra_context['top_searches'] = SearchHistory.get_top_searches()
        extra_context['searches_by_type'] = SearchHistory.get_searches_by_type()
        
        return super().changelist_view(request, extra_context=extra_context)
