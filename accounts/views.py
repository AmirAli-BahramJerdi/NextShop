from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Profile, Address
from .forms import ProfileForm, AddressForm


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        # Get or create profile for current user
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, 'پروفایل شما با موفقیت بروزرسانی شد.')
        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session to prevent logout
            update_session_auth_hash(request, user)
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت.')
            return redirect('profile')
        return render(request, 'accounts/change_password.html', {'form': form})


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'accounts/address_list.html'
    context_object_name = 'addresses'
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'accounts/address_form.html'
    success_url = reverse_lazy('address_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'آدرس جدید با موفقیت اضافه شد.')
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'accounts/address_form.html'
    success_url = reverse_lazy('address_list')
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'آدرس با موفقیت بروزرسانی شد.')
        return super().form_valid(form)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'accounts/address_confirm_delete.html'
    success_url = reverse_lazy('address_list')
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'آدرس با موفقیت حذف شد.')
        return super().delete(request, *args, **kwargs)