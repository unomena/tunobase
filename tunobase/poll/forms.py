'''
Created on 26 Mar 2013

@author: michael
'''
import collections

from django import forms

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
                    queryset=self.poll.permitted_answers, 
                    widget=forms.CheckboxSelectMultiple
                )
            else:
                self.fields['answers'] = forms.ModelChoiceField(
                    queryset=self.poll.permitted_answers, 
                    widget=forms.RadioSelect, 
                    empty_label=None
                )
                
            self.fields['answers'].widget.attrs.update({'class': 'required'})
            
    def increment_vote_count(self, answer):
        answer.vote_count += 1
        answer.save()
            
    def save(self):
        answers = self.cleaned_data['answers']
        
        if isinstance(answers, collections.Iterable):
            for answer in answers:
                self.increment_vote_count(answer)
        else:
            self.increment_vote_count(answers)
        
        return answers