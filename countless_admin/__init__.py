from django.contrib.admin.views.main import ChangeList
from django.core.paginator import Page, Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext_lazy as _


class CountlessPage(Page):
    """
    Page without count()

    Next page presence is detected as object_list contains more than per_page
    objects.
    """
    @property
    def object_list(self):
        """
        Removes exceeding elements from object_list
        """
        try:
            return self.__object_list[:self.paginator.per_page]
        except TypeError:
            return list()

    @object_list.setter
    def object_list(self, value):
        self.__object_list = value

    def __init__(self, object_list, number, paginator):
        self.__object_list = None
        super(CountlessPage, self).__init__(object_list, number, paginator)

    def __repr__(self):
        return '<Page %s of Unknown>' % (self.number,)

    def has_next(self):
        try:
            return len(self.__object_list) > self.paginator.per_page
        except TypeError:
            return False

    def end_index(self):
        raise NotImplementedError("feed doesn't support count")


class CountlessAdminPaginator(Paginator):
    """
    Paginator without count()

    """

    num_pages = 100

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        :param number:
        :return:
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))
        if number < 1:
            raise EmptyPage(_('That page number is less than 1'))
        return number

    def page(self, number):
        """Returns a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        # top + 1 for detecting next page presence.
        if self.object_list is not None:
            return CountlessPage(self.object_list[bottom: top + 1],
                                 number, self)
        return CountlessPage(None, number, self)


class CountlessChangeList(ChangeList):
    """
    Django admin ChangeList without count().
    """

    # noinspection PyAttributeOutsideInit
    def get_results(self, request):
        """
        Replace count() calls with len(self.result_list).
        """

        self.paginator = self.model_admin.get_paginator(
            request, self.queryset, self.list_per_page)

        # noinspection PyBroadException
        try:
            page = self.paginator.page(self.page_num + 1)
            self.result_list = list(page.object_list)
        except Exception:
            self.result_list = list()

        self.result_count = self.full_result_count = len(self.result_list)

    multi_page = True
    can_show_all = True
    show_all = True
    show_admin_actions = True


class CountlessAdminMixin:
    """
    Replaces paginator and changelist classes with no-count() versions.
    """

    paginator = CountlessAdminPaginator

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get_changelist(self, request, **kwargs):
        return CountlessChangeList
