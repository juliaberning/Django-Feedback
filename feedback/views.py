from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Review, UserProfile, FeedbackProcess
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CombinedProfileForm, CustomUserCreationForm, ReviewForm


def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'feedback/home.html', {'username': username})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save() 
            messages.success(request, f'Account created for {user.username}!')

            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)

            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'feedback/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.warning(request, 'Invalid username or password.')
    return render(request, 'feedback/login.html')

def logout_view(request):
    logout(request)
    return redirect('home') 


@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = CombinedProfileForm(request.POST, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
    else:
        form = CombinedProfileForm(instance=user_profile, user=request.user)

    return render(request, 'feedback/profile.html', {'form': form})

@login_required
def user_list(request):
    users = UserProfile.objects.all()

    for user in users:
        feedback_process = FeedbackProcess.objects.filter(reviewee=user).first()
        
        if feedback_process:
            reviewers = Review.objects.filter(feedback_process=feedback_process)
            user.reviewers = [review.reviewer.user.username for review in reviewers]
        else:
            user.reviewers = []

    return render(request, 'feedback/user-list.html', {'users': users})



@login_required
def create_feedback_process(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.info(request, "You need to complete your profile.")
        return redirect('profile')

    existing_feedback_process = FeedbackProcess.objects.filter(reviewee=user_profile).first()
    
    if request.method == 'POST':
        if existing_feedback_process:
            messages.warning(request, "You already have an existing feedback process.")
        else:
            FeedbackProcess.objects.create(
                reviewee=user_profile,
                manager=user_profile.manager 
            )
            messages.success(request, "A new feedback process has been created!")
    
    return render(request, 'feedback/create-feedback-process.html', {
        'user_profile': user_profile
    })

@login_required
def select_reviewer(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.info(request, "You need to complete your profile.")
        return redirect('profile')

    feedback_process = FeedbackProcess.objects.filter(reviewee=user_profile).first()

    if not feedback_process:
        messages.error(request, "You do not have an existing feedback process.")
        return redirect('create-feedback-process')

    potential_reviewers = UserProfile.objects.all()

    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        if reviewer_id:
            reviewer = UserProfile.objects.get(id=reviewer_id)
            
            
            try:
                Review.objects.create(
                    feedback_process=feedback_process,
                    reviewer=reviewer,    
                )
                messages.success(request, f"Reviewer {reviewer.user.username} has been selected.")
                return redirect('user-list')

            except IntegrityError:
                messages.warning(request, f"Reviewer {reviewer.user.username} has already been assigned for this feedback process.")
                return redirect('select-reviewer')
            
        else:
            messages.error(request, "Please select a reviewer.")
    
    return render(request, 'feedback/select-reviewer.html', {
        'user_profile': user_profile, #TODO:evaluate if this is needed
        'feedback_process': feedback_process,
        'potential_reviewers': potential_reviewers,
    })

@login_required
def create_review(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.info(request, "You need to complete your profile.")
        return redirect('profile')

    # Fetch all reviews where the logged-in user is the reviewer
    reviews = Review.objects.filter(reviewer=user_profile)

    # Extract reviewees (the users who selected the logged-in user as their reviewer)
    reviewees = [review.feedback_process.reviewee for review in reviews]

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        reviewee_id = request.POST.get('reviewee')

        if form.is_valid() and reviewee_id:
            reviewee = UserProfile.objects.get(id=reviewee_id)
            feedback_process = FeedbackProcess.objects.get(reviewee=reviewee)

            existing_review = Review.objects.filter(
                reviewer=user_profile, feedback_process=feedback_process
            ).first()
            existing_review.reviewee_strengths_text = form.cleaned_data['reviewee_strengths_text']
            existing_review.reviewee_improvements_text = form.cleaned_data['reviewee_improvements_text']
            existing_review.reviewee_growth_rating = form.cleaned_data['reviewee_growth_rating']
            existing_review.reviewee_execution_rating = form.cleaned_data['reviewee_execution_rating']
            existing_review.reviewee_collaboration_rating = form.cleaned_data['reviewee_collaboration_rating']
            existing_review.save()
            messages.success(request, f"Review for {reviewee.user.username} has been updated.")

    else:
        form = ReviewForm()

    return render(request, 'feedback/create-review.html', {'reviewees': reviewees, 'form': form})
