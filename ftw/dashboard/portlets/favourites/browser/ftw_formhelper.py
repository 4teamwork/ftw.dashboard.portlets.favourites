from zope.component import getMultiAdapter

from Acquisition import aq_inner, aq_parent
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.portlets.browser.formhelper import AddForm, NullAddForm, EditForm

from ftw.dashboard.portlets.favourites import _


class ftwAddForm(AddForm):

    def nextURL(self):
        status = IStatusMessage(self.request)
        status.addStatusMessage(_(u'Portlet added to dashboard'), type='info')
        referer = self.request.form.get('referer')
        if referer:
            return referer
        else:
            portlet = aq_inner(self.context)
            context = aq_parent(portlet)
            url = str(getMultiAdapter((context, self.request), name=u"absolute_url"))
            return url + '/@@manage-portlets'


class ftwEditForm(EditForm):

    def nextURL(self):
        status = IStatusMessage(self.request)
        title = 'bla'
        status.addStatusMessage(_(u'Portlet edited'), type='info')

        referer = self.request.form.get('referer')
        if referer:
            return referer
        else:
            portlet = aq_inner(self.context)
            context = aq_parent(portlet)
            url = str(getMultiAdapter((context, self.request), name=u"absolute_url"))
            return url + '/@@manage-portlets'


class ftwNullAddForm(NullAddForm):

    def nextURL(self):
        status = IStatusMessage(self.request)
        title = 'bla'
        status.addStatusMessage(_(u'Portlet added to dashboard'), type='info')
        referer = self.request.get('referer')
        if referer:
            return referer
        else:
            addview = aq_parent(aq_inner(self.context))
            context = aq_parent(aq_inner(addview))
            url = str(getMultiAdapter((context, self.request), name=u"absolute_url"))
            return url + '/@@manage-portlets'
