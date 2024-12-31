from .models import Entry, Vote
from django.http import JsonResponse


from django.shortcuts import render, redirect, get_object_or_404
from .forms import EntryForm, UserCreationFormMail

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
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('home')
    else:
        form = EntryForm()
    return render(request, 'dictionary/add_entry.html', {'form': form})


def home(request):
    entries = Entry.objects.all()

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