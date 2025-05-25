# Create your views here.

from django.shortcuts import render
from django import forms
from django.http import HttpResponse

class UserInputForm(forms.Form):
    user_input = forms.CharField(max_length=100)

def secure_input_view(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Process the valid input
            safe_input = form.cleaned_data['user_input']
            return HttpResponse(f"Safe input received: {safe_input}")
    else:
        form = UserInputForm()
    return render(request, 'myapp/input_form.html', {'form': form})