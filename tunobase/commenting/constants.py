"""
Commenting App

This module lists the default settings for the commenting app.

"""
FLAG_SUGGEST_REMOVAL = "removal suggestion"
FLAG_MODERATOR_DELETION = "moderator deletion"
FLAG_MODERATOR_APPROVAL = "moderator approval"

FLAG_CHOICES = (
    (FLAG_SUGGEST_REMOVAL, "Removal Suggestion"),
    (FLAG_MODERATOR_DELETION, "Moderator Deletion"),
    (FLAG_MODERATOR_APPROVAL, "Moderator Approval"),
)
