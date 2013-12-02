'''
Created on 28 Oct 2013

@author: michael
'''
from tunobase.core import managers as core_managers

class PollAnswerManager(core_managers.CoreStateManager):
    
    def get_poll_percentages(self):
        total_vote_counts = 0
        vote_count_averages = []
        poll_answers = self.permitted()
        
        for poll_answer in poll_answers:
            total_vote_counts += poll_answer.vote_count
        
        for poll_answer in poll_answers:
            try:
                vote_count_averages.append(
                    float('%0.2f' % ((poll_answer.vote_count / float(total_vote_counts)) * 100))
                )
            except ZeroDivisionError:
                vote_count_averages.append(0.0)
        
        return vote_count_averages