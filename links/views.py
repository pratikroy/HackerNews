from django.urls import reverse
from django.shortcuts import render
from links.models import Link, Comment
from django.utils.decorators import method_decorator
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, View
from django.contrib.auth.decorators import login_required
from links.forms import LinkSubmissionForm, CommentModelForm

# Create your views here.
class NewSubmissionView(CreateView):
    form_class = LinkSubmissionForm
    template_name = 'links/new_submission.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewSubmissionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_link = form.save(commit=False)
        new_link.submitted_by = self.request.user
        new_link.save()

        self.object = new_link
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('submission-detail', kwargs={'pk':self.object.pk})


class SubmissionDetailView(DetailView):
    model = Link
    template_name = 'links/submission_detail.html'
    context_object_name = 'link_detail'

    def get_context_data(self, **kwargs):
        ctx = super(SubmissionDetailView, self).get_context_data(**kwargs)
        submission_comments = Comment.objects.filter(commented_on=self.object, in_reply_to__isnull=True)
        ctx['comments'] = submission_comments
        ctx['comment_form'] = CommentModelForm(initial={'link_pk':self.object.pk})

        return ctx


class NewCommentView(CreateView):
    form_class = CommentModelForm
    http_method_names = ('post')
    template_name = 'links/comment.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        parent_link = Link.objects.get(pk=form.cleaned_data['link_pk'])
        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_link
        new_comment.commented_by = self.request.user
        new_comment.save()

        return HttpResponseRedirect(reverse('submission-detail', kwargs={'pk':parent_link.pk}))

    def get_initial(self):
        initial_data = super(NewCommentView, self).get_initial()
        initial_data['link_pk'] = self.request.GET['link_pk']
        return initial_data

    def get_context_data(self, **kwargs):
        ctx = super(NewCommentView, self).get_context_data(**kwargs)
        ctx['submission'] = Link.objects.get(pk=self.request.GET['link_pk'])

        return ctx


class AllLinkListView(ListView):
    model = Link
    template_name = 'home.html'
    context_object_name = 'all_links'

    def get_queryset(self):
        return Link.objects.order_by('-submitted_on')


class NewCommentReplyView(CreateView):
    form_class = CommentModelForm
    template_name = 'links/comment_reply.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentReplyView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(NewCommentReplyView, self).get_context_data(**kwargs)
        ctx['parent_comment'] = Comment.objects.get(pk=self.request.GET['parent_comment_pk'])
        return ctx

    def get_initial(self):
        initial_data = super(NewCommentReplyView, self).get_initial()
        link_pk = self.request.GET['link_pk']
        initial_data['link_pk'] = link_pk
        parent_comment_pk = self.request.GET['parent_comment_pk']
        initial_data['parent_comment_pk'] = parent_comment_pk
        return initial_data

    def form_valid(self, form):
        parent_link = Link.objects.get(pk=form.cleaned_data['link_pk'])
        parent_comment = Comment.objects.get(pk=form.cleaned_data['parent_comment_pk'])
        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_link
        new_comment.in_reply_to = parent_comment
        new_comment.commented_by = self.request.user
        new_comment.save()

        return HttpResponseRedirect(reverse('submission-detail',kwargs={'pk':parent_link.pk}))


class UpvoteSubmissionView(View):
    @method_decorator(login_required)
    def get(self, request, link_pk, **kwargs):
        link = Link.objects.get(pk=link_pk)
        link.upvotes.add(request.user)

        return HttpResponseRedirect(reverse('home'))


class RemoveUpvoteFromSubmissionView(View):
    @method_decorator(login_required)
    def get(self, request, link_pk, **kwargs):
        link = Link.objects.get(pk=link_pk)
        link.upvotes.remove(request.user)

        return HttpResponseRedirect(reverse('home'))
