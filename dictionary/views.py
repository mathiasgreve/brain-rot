from .models import Entry, Vote, Example
from django.http import JsonResponse

from django.forms import modelformset_factory


from django.shortcuts import render, redirect, get_object_or_404
from .forms import EntryForm, UserCreationFormMail, ExampleForm

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def loginView(request):
    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationFormMail(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = UserCreationFormMail()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_entry(request):
    ExampleFormSet = modelformset_factory(Example, form=ExampleForm, extra=1, can_delete=True)
    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        example_formset = ExampleFormSet(request.POST, queryset=Example.objects.none())
        
        if entry_form.is_valid() and example_formset.is_valid():
            entry = entry_form.save(commit=False)
            entry.author = request.user
            entry.save()

            for form in example_formset:
                if form.cleaned_data:  # Skip empty forms
                    example = form.save(commit=False)
                    example.entry = entry
                    example.save()

            return redirect('home')
    else:
        entry_form = EntryForm()
        example_formset = ExampleFormSet(queryset=Example.objects.none())

    return render(request, 'dictionary/add_entry.html', {
        'entry_form': entry_form,
        'example_formset': example_formset,
    })

def home(request):
    entries = Entry.objects.prefetch_related('examples').all()

    # Add vote counts to each entry
    for entry in entries:
        entry.upvote_count = Vote.objects.filter(entry=entry, vote_type=Vote.UPVOTE).count()
        entry.downvote_count = Vote.objects.filter(entry=entry, vote_type=Vote.DOWNVOTE).count()

    return render(request, 'dictionary/home.html', {'entries': entries})


@login_required
def upvote_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    # Check if the user already has a vote on this entry
    try:
        vote = Vote.objects.get(entry=entry, user=request.user)
        # The user has already voted on this entry
        if vote.vote_type == Vote.UPVOTE:
            # If the vote is UPVOTE, remove the vote
            print(f"Removing upvote for entry {entry_id} by user {request.user.username}")
            vote.delete()
        elif vote.vote_type == Vote.DOWNVOTE:
            # Change from DOWNVOTE to UPVOTE
            print(f"Changing vote from DOWNVOTE to UPVOTE for entry {entry_id} by user {request.user.username}")
            vote.vote_type = Vote.UPVOTE
            vote.save()
    except Vote.DoesNotExist:
        # No vote found, create a new one
        print(f"Creating an upvote for entry {entry_id} by user {request.user.username}")
        Vote.objects.create(entry=entry, user=request.user, vote_type=Vote.UPVOTE)

    return redirect('home')  # Redirect back to the home page



@login_required
def downvote_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    # Check if the user already has a vote on this entry
    try:
        vote = Vote.objects.get(entry=entry, user=request.user)
        # The user has already voted on this entry
        if vote.vote_type == Vote.DOWNVOTE:
            # If the vote is UPVOTE, remove the vote
            print(f"Removing upvote for entry {entry_id} by user {request.user.username}")
            vote.delete()
        elif vote.vote_type == Vote.UPVOTE:
            # Change from UPVOTE to DOWNVOTE
            print(f"Changing vote from UPVOTE to DOWNVOTE for entry {entry_id} by user {request.user.username}")
            vote.vote_type = Vote.DOWNVOTE
            vote.save()
    except Vote.DoesNotExist:
        # No vote found, create a new one
        print(f"Creating an upvote for entry {entry_id} by user {request.user.username}")
        Vote.objects.create(entry=entry, user=request.user, vote_type=Vote.DOWNVOTE)

    return redirect('home')  # Redirect back to the home page

"""
@login_required
def downvote_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    vote, created = Vote.objects.get_or_create(entry=entry, user=request.user, defaults={'vote_type': Vote.DOWNVOTE})
    print(f"{request.user.username} downvoted for entry {entry_id}")
    if not created:  # The user already has a vote
        if vote.vote_type == Vote.UPVOTE:
            print(f"Changing vote from UPVOTE to DOWNVOTE for entry {entry_id} by user {request.user.username}")

            vote.vote_type = Vote.DOWNVOTE
            vote.save()
        elif vote.vote_type == Vote.DOWNVOTE:
            print(f"Removing downvote for entry {entry_id} by user {request.user.username}")

            vote.delete()  # Remove the downvote
    return redirect('home')  # Redirect back to the home page
"""



"""
@login_required
def upvote_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    vote, created = Vote.objects.get_or_create(entry=entry, user=request.user, defaults={'vote_type': Vote.UPVOTE})
    
    if not created:  # The user already has a vote
        if vote.vote_type == Vote.DOWNVOTE:
            vote.vote_type = Vote.UPVOTE
            vote.save()
        elif vote.vote_type == Vote.UPVOTE:
            vote.delete()  # Remove the upvote

    # Return updated vote counts as JSON response
    upvote_count = Vote.objects.filter(entry=entry, vote_type=Vote.UPVOTE).count()
    downvote_count = Vote.objects.filter(entry=entry, vote_type=Vote.DOWNVOTE).count()

    return JsonResponse({'upvote_count': upvote_count, 'downvote_count': downvote_count})

@login_required
def downvote_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    vote, created = Vote.objects.get_or_create(entry=entry, user=request.user, defaults={'vote_type': Vote.DOWNVOTE})
    
    if not created:  # The user already has a vote
        if vote.vote_type == Vote.UPVOTE:
            vote.vote_type = Vote.DOWNVOTE
            vote.save()
        elif vote.vote_type == Vote.DOWNVOTE:
            vote.delete()  # Remove the downvote

    # Return updated vote counts as JSON response
    upvote_count = Vote.objects.filter(entry=entry, vote_type=Vote.UPVOTE).count()
    downvote_count = Vote.objects.filter(entry=entry, vote_type=Vote.DOWNVOTE).count()

    return JsonResponse({'upvote_count': upvote_count, 'downvote_count': downvote_count})

"""