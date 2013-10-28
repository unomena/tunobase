'''
Created on 28 Oct 2013

@author: michael
'''
FLAG_SUGGEST_REMOVAL = "removal suggestion"
FLAG_LIKE = "like"
FLAG_DISLIKE = "dislike"
FLAG_MODERATOR_DELETION = "moderator deletion"
FLAG_MODERATOR_APPROVAL = "moderator approval"

FLAG_CHOICES = (
    (FLAG_LIKE, "Liked by User"),
    (FLAG_DISLIKE, "Disliked by User"),
    (FLAG_SUGGEST_REMOVAL, "Removal Suggestion"),
    (FLAG_MODERATOR_DELETION, "Moderator Deletion"),
    (FLAG_MODERATOR_APPROVAL, "Moderator Approval"),
)