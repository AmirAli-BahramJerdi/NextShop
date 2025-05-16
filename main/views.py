from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from products.models import Product, Category
from .models import Banner, Feature, PromoBanner, Newsletter
from .forms import NewsletterForm


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(is_active=True)
        context['features'] = Feature.objects.all()
        context['special_offers'] = Product.objects.filter(is_special_offer=True)[:4]
        context['promo_banner'] = PromoBanner.objects.filter(is_active=True).first()
        context['categories'] = Category.objects.filter(is_featured=True)[:6]
        context['newsletter_form'] = NewsletterForm()
        return context


class NewsletterView(View):
    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ایمیل شما با موفقیت در خبرنامه ثبت شد.')
        else:
            messages.error(request, 'خطا در ثبت ایمیل. لطفا دوباره تلاش کنید.')
        
        return redirect('home')