"""
Commenting App

This module provides an interface to flagging and fetching comments.

Classes:
    PostComment
    ReportComment
    LoadMoreComments

Functions:
    n/a

Created on 29 Oct 2013

@author: michael

"""
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views import generic as generic_views

from tunobase.core import utils as core_utils, mixins as core_mixins
from tunobase.commenting import models, exceptions


class PostComment(core_mixins.DeterministicLoginRequiredMixin,
        generic_views.FormView):
    """Provide post comment form functionality."""

    def deterministic_function(self):
        """Determine if comments are allowed."""

        return settings.ANONYMOUS_COMMENTS_ALLOWED

    def post(self, request, *args, **kwargs):
        """Receive posted form."""

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.ajax_form_valid(form) \
                if request.is_ajax() else self.form_valid(form)
        else:
            return self.ajax_form_invalid(form) \
                if request.is_ajax() else self.form_invalid(form)

    def form_valid(self, form):
        """Determine if the comment form is valid and redirect."""
        try:
            form.save(self.request)
            messages.success(self.request, 'Your comment has been posted')
        except exceptions.RapidCommentingError as e:
            messages.error(self.request, e)

        return redirect(form.cleaned_data['next'] \
                or self.request.META['HTTP_REFERER'])

    def form_invalid(self, form):
        """Redirect if comment form is invalid."""

        messages.error(self.request, str(form.errors))

        return redirect(self.request.META['HTTP_REFERER'])

    def ajax_form_valid(self, form):
        """Allow for ajax form posts and check if form is valid."""

        try:
            comment = form.save(self.request)
            num_comments = models.CommentModel.objects.permitted().count()

            return core_utils.respond_with_json({
                'success': True,
                'comment': render_to_string(
                    self.template_name,
                    RequestContext(self.request, {'comment': comment})
                ),
                'num_comments': num_comments
            })
        except exceptions.RapidCommentingError as e:
            return core_utils.respond_with_json({
                'success': False,
                'reason': e.value
            })

    def ajax_form_invalid(self, form):
        """Redirect if form invalid."""

        return core_utils.respond_with_json({
            'success': False,
            'reason': str(form.errors)
        })


class ReportComment(core_mixins.LoginRequiredMixin, generic_views.View):
    """Flag a comment to be removed."""

    def get(self, request, *args, **kwargs):
        """Flag a particular comment."""

        try:
            models.CommentFlag.objects.report(
                request.user,
                self.kwargs['pk'],
            )
        except IntegrityError:
            if request.is_ajax():
                return core_utils.respond_with_json({
                    'success': False,
                    'reason': 'You have already reported this comment'
                })

            messages.error(request, 'You have already reported this comment')
            return redirect(request.META['HTTP_REFERER'])

        if request.is_ajax():
            return core_utils.respond_with_json({
                'success': True
            })

        messages.success(request, 'This comment has been reported')
        return redirect(request.META['HTTP_REFERER'])


class LoadMoreComments(core_mixins.AjaxMorePaginationMixin,
                       generic_views.ListView):
    """Display more comments."""

    def get_queryset(self):
        """Get more comments."""

        return models.CommentModel.objects.permitted().get_comments_for_object(
            self.request.GET['content_type_id'],
            self.request.GET['object_pk'],
        )
