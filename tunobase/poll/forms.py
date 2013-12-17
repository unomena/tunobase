'''
Created on 26 Mar 2013

@author: michael
'''
from django import forms
from django.contrib import messages
from django.conf import settings

class PollAnswerForm(forms.Form):
    '''
    Form for handling Poll answers
    '''
    multiple_answers = forms.BooleanField(
            widget=forms.HiddenInput, required=False
    )

    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll', None)
        self.multiple_answers = kwargs.pop('multiple_answers', None)
        super(PollAnswerForm, self).__init__(*args, **kwargs)

        if self.poll is not None:
            if self.poll.multiple_choice:
                self.fields['answers'] = forms.ModelMultipleChoiceField(
                    queryset=self.poll.answers.permitted(),
                    widget=forms.CheckboxSelectMultiple
                )
            else:
                self.fields['answers'] = forms.ModelChoiceField(
                    queryset=self.poll.answers.permitted(),
                    widget=forms.RadioSelect,
                    empty_label=None
                )

            self.fields['answers'].widget.attrs.update({'class': 'required'})

        if self.multiple_answers is not None:
            self.fields['multiple_answers'].initial = self.multiple_answers

    def increment_vote_count(self, answer):
        answer.vote_count += 1
        answer.save()

    def save(self, request, cookie_name, pk):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        multiple_answers_allowed = getattr(
                settings, 'ALLOW_CERTAIN_POLL_MULTIPLE_ANSWERS', False
        )

        if multiple_answers_allowed and self.cleaned_data['multiple_answers']:
            poll_voted = False
        elif user is None:
            poll_voted = request.COOKIES.get(cookie_name, False)
        else:
            poll_voted = user.polls_answered.filter(pk=pk).exists()

        if poll_voted:
            messages.error(request, 'You have already voted in this poll.')
        else:
            answers = self.cleaned_data['answers']
            if isinstance(answers, (list, tuple)):
                for answer in answers:
                    self.increment_vote_count(answer)
            else:
                self.increment_vote_count(answers)

            if user is not None:
                self.poll.users_answered.add(user)

            messages.success(request, 'You have voted.')
