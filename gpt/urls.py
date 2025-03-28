from django.urls import path
from .views import GPTIssueView, GPTPromptView

urlpatterns = [
    path('issue', GPTIssueView.as_view(), name='gpt_issue'),
    path('prompt', GPTPromptView.as_view(), name='gpt_prompt'),
]