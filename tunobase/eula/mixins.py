'''
Created on 23 Oct 2013

@author: michael
'''
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from tunobase.eula import models, utils

class EULAAcceptedMixin(object):
    eula_url = 'eula_sign'
    raise_exception = False

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.eula = get_object_or_404(models.EULA).latest_version()

        # If the user has accepted the latest EULA
        if not models.UserEULA.objects\
                .filter(user=request.user, eula=self.eula)\
                .exists():
            if self.raise_exception:
                raise PermissionDenied
            else:
                if hasattr(self, 'get_object'):
                    self.object = self.get_object()
                    eula_url_kwargs = {
                        'content_type_id': ContentType.objects\
                                .get_for_model(self.object).id,
                        'object_pk': self.object.pk
                    }
                    eula_url = reverse_lazy(
                            self.eula_url, kwargs=eula_url_kwargs
                    )
                else:
                    eula_url = reverse_lazy(self.eula_url)

                return utils.redirect_to_eula(
                    request.get_full_path(),
                    eula_url
                )

        return super(EULAAcceptedMixin, self).dispatch(
            request,
            *args,
            **kwargs
        )
