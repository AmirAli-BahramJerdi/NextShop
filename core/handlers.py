from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

def error_404(request, exception):
    """ویو صفحه 404"""
    return render(request, 'errors/404.html', {'title': _('صفحه مورد نظر یافت نشد')}, status=404)


def error_500(request):
    """ویو صفحه 500"""
    return render(request, 'errors/500.html', {'title': _('خطای سرور')}, status=500)


def error_403(request, exception):
    """ویو صفحه 403"""
    return render(request, 'errors/403.html', {'title': _('دسترسی غیرمجاز')}, status=403)


def error_400(request, exception):
    """ویو صفحه 400"""
    return render(request, 'errors/400.html', {'title': _('درخواست نامعتبر')}, status=400)