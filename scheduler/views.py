from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Course, Subject, Topic, CustomUser
from .forms import CourseForm, SubjectForm, TopicForm, UserRegistrationForm, LoginForm
from django.utils.timezone import now
from django.http import JsonResponse
import json


def home(request):
    return render(request, 'scheduler/home.html')  # Renders home page
# Admin Dashboard
@login_required
def admin_dashboard(request):
    return render(request, 'scheduler/admin_dashboard.html')

# User Dashboard
@login_required
def user_dashboard(request):
    courses = Course.objects.all()
    subjects = []
    topics = []

    selected_course_id = request.GET.get('course_id')
    selected_subject_id = request.GET.get('subject_id')

    selected_course = None
    selected_subject = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)
        subjects = Subject.objects.filter(course=selected_course)

    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
        topics = Topic.objects.filter(subject=selected_subject)

    return render(request, 'scheduler/user_dashboard.html', {
        'courses': courses,
        'subjects': subjects,
        'topics': topics,
        'selected_course': selected_course,
        'selected_subject': selected_subject,
        'selected_course_id': selected_course_id,
        'selected_subject_id': selected_subject_id,
    })

# Add Course (Admin Only)
@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'scheduler/add_course.html', {'form': form})

# Add Subject (Admin Only)
@login_required
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SubjectForm()
    return render(request, 'scheduler/add_subject.html', {'form': form})

# Add Topic (Admin Only)
@login_required
def add_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # ✅ Fix redirection here
    else:
        form = TopicForm()
    return render(request, 'scheduler/add_topic.html', {'form': form})
# Mark Topic as Done (Users)
@login_required
def mark_done(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.mark_completed()
    return redirect('user_dashboard')

# User Progress
@login_required
def user_progress(request):
    # Get topics for the current user that have time added
    topics = Topic.objects.filter(hours_spent__gt=0)
    
    # Debug: Print the number of topics
    print(f"Number of topics with time added: {topics.count()}")
    
    # Calculate progress statistics
    completed_topics = topics.filter(is_completed=True).count()
    total_topics = topics.count()
    total_hours_spent = sum(topic.hours_spent for topic in topics)
    
    # Calculate progress percentage
    progress = (completed_topics / total_topics * 100) if total_topics > 0 else 0
    
    # Get topics by subject for detailed progress
    subjects = Subject.objects.filter(topic__in=topics).distinct()
    subject_progress = []
    
    for subject in subjects:
        subject_topics = topics.filter(subject=subject)
        completed = subject_topics.filter(is_completed=True).count()
        total = subject_topics.count()
        subject_progress.append({
            'subject': subject,
            'completed': completed,
            'total': total,
            'percentage': (completed / total * 100) if total > 0 else 0
        })
    
    # Prepare topic data for the chart, organized by subject
    topic_data = []
    
    # Group topics by subject
    for subject in subjects:
        subject_topics = topics.filter(subject=subject)
        
        # Sort topics by hours spent
        sorted_subject_topics = sorted(subject_topics, key=lambda x: x.hours_spent)
        
        # Add subject name as a data point
        topic_data.append({
            'name': f"{subject.name}",
            'hours_spent': 0,
            'cumulative_hours': 0,
            'is_completed': False,
            'subject_name': subject.name,
            'is_subject': True
        })
        
        # Add topics for this subject
        cumulative_hours = 0
        for topic in sorted_subject_topics:
            cumulative_hours += topic.hours_spent
            topic_data.append({
                'name': topic.name,
                'hours_spent': topic.hours_spent,
                'cumulative_hours': round(cumulative_hours, 2),
                'is_completed': topic.is_completed,
                'subject_name': subject.name,
                'is_subject': False
            })
    
    # Debug: Print topic data
    print(f"Topic data: {topic_data}")
    
    # Extract data for the chart
    topic_names = []
    topic_hours = []
    topic_completed = []
    
    for item in topic_data:
        if item['is_subject']:
            # For subjects, use a different format
            topic_names.append(f"📚 {item['subject_name']}")
        else:
            # For topics, show the topic name
            topic_names.append(f"  • {item['name']}")
        
        topic_hours.append(item['cumulative_hours'])
        topic_completed.append(item['is_completed'])
    
    # Debug: Print chart data
    print(f"Topic names: {topic_names}")
    print(f"Topic hours: {topic_hours}")
    print(f"Topic completed: {topic_completed}")
    
    # Convert lists to JSON strings for template
    topic_names_json = json.dumps(topic_names)
    topic_hours_json = json.dumps(topic_hours)
    topic_completed_json = json.dumps(topic_completed)
    
    # Add user information to the context
    context = {
        'progress': round(progress, 2),
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'total_hours_spent': round(total_hours_spent, 2),
        'subject_progress': subject_progress,
        'topic_names': topic_names_json,
        'topic_hours': topic_hours_json,
        'topic_completed': topic_completed_json,
        'username': request.user.username
    }
    
    return render(request, 'scheduler/progress_chart.html', context)

# User Registration
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['is_admin']:
                user.is_admin = True
            user.save()
            return redirect('login')  # Redirect to login page
    else:
        form = UserRegistrationForm()
    return render(request, 'scheduler/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user type
            if user.is_admin:
                return redirect('admin_dashboard')  # Admin Redirect
            else:
                return redirect('user_dashboard')  # User Redirect

    else:
        form = LoginForm()
    return render(request, 'scheduler/login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_time(request, topic_id):
    if request.method == "POST":
        topic = get_object_or_404(Topic, id=topic_id)
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        
        topic.add_time_spent(hours, minutes)
        return JsonResponse({
            'status': 'success', 
            'hours_spent': topic.hours_spent
        })
    return JsonResponse({'status': 'error'})