
# from django.shortcuts import redirect
# from django.contrib import messages





# #ccbv:
# from django.contrib.auth.views import LoginView,PasswordChangeView, PasswordResetView,PasswordResetConfirmView
# from django.views.generic import TemplateView,UpdateView, ListView,DetailView,DeleteView

# from django.urls import reverse_lazy



# from django.contrib.auth import get_user_model
# User = get_user_model()

    
# class ProfileView(TemplateView):
#     template_name = 'accounts/profile.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         context['username'] = user.username
#         context['email'] = user.email
#         context['name'] = user.get_full_name()
#         context['member_since'] = user.date_joined
#         context['last_login'] = user.last_login
#         # context['bio'] = user.userprofile.bio
#         context['bio'] = user.bio
#         # context['profile_image'] = user.userprofile.profile_image
#         context['profile_image'] = user.profile_image
#         context['phone_no'] = user.phone_no
#         return context

# class EditProfileView(UpdateView):
#     model = User
#     form_class=EditProfileForm
#     template_name = 'accounts/update_profile.html'
#     context_object_name = 'form'
#     def get_object(self):
#         return self.request.user

#     def form_valid(self, form):
#         form.save()
#         return redirect('profile')

# #password change
    
# class ChangePassword(PasswordChangeView):
#     template_name = 'accounts/password_change.html'
#     form_class = CustomPasswordChangeForm


# class CustomPasswordResetView(PasswordResetView):
#     form_class = CustomPasswordResetForm
#     template_name = 'registration/reset_password.html'
#     html_email_template_name = "registration/reset_email.html"

#     success_url = reverse_lazy('signin')

#     def form_valid(self,form):
#         messages.success(self.request, 'A reset email sent.Please Check Your Email.' )
#         return super().form_valid(form)
     
# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     form_class = CustomPasswordResetConfirmForm
#     template_name = 'registration/reset_password.html'
#     success_url = reverse_lazy('signin')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['protocol'] = 'https' if self.request.is_secure() else 'http'
#         context['domain'] = self.request.get_host()
#         print(context)
#         return context


#     def form_valid(self,form):
#         messages.success(self.request, 'Password has been reset successfully.' )
#         return super().form_valid(form)
      