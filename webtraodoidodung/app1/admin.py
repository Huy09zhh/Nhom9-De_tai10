from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(TradeAddress)

class ProfileAdminForm(forms.ModelForm):
    amount = forms.DecimalField(
        label="Thay đổi số dư",
        required=False,
        help_text="Nhập số tiền muốn tăng (+) hoặc giảm (-)",
    )

    class Meta:
        model = Profile
        fields = ['balance']

    def save(self, commit=True):
        profile = super().save(commit=False)
        amount = self.cleaned_data.get('amount')
        if amount is not None:
            profile.balance += amount  # Cộng/trừ số dư
        if commit:
            profile.save()
        return profile

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('user', 'balance')

admin.site.register(Profile, ProfileAdmin)