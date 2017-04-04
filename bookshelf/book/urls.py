from django.conf.urls import url
from bookshelf.book.views.book import (
    BookAddView, BookQueryView, BookListView, BookDetailView
)

urlpatterns = [
    url(r'^query$', BookQueryView.as_view()),
    url(r'^add$', BookAddView.as_view()),
    url(r'^list$', BookListView.as_view()),
    url(r'^detail$', BookDetailView.as_view()),
]
