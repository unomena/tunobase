'''
Created on 26 Mar 2013

@author: michael
'''
from django import forms
from django.contrib import messages

from preferences import preferences

class PollAnswerForm(forms.Form):
    '''
    Form for handling Poll answers
    '''
    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll', None)
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
            
    def increment_vote_count(self, answer):
        answer.vote_count += 1
        answer.save()
            
    def save(self, request):
        session_key = 'poll_%s_voted' % self.kwargs['pk']
        poll_voted = request.session.get(session_key, False)
        if poll_voted:
            messages.error(request, 'You have already voted in this poll.')
            return None
        
        answers = self.cleaned_data['answers']
        if isinstance(answers, (list, tuple)):
            for answer in answers:
                self.increment_vote_count(answer)
        else:
            self.increment_vote_count(answers)
            
        request.session[session_key] = True
        messages.success(request, 'You have voted.')
        
        return answers