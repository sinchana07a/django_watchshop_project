from django import forms
from .models import Watches,RatingComment

class WatchForm(forms.ModelForm):
    class Meta:
        model = Watches
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            }
        
class RatingCommentForm(forms.ModelForm):
    rating=forms.ChoiceField(choices=[(i,str(i)) for i in range(6)],label='Rating')
    class Meta:
        model=RatingComment
        fields=['rating','comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            }