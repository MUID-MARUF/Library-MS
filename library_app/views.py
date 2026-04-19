from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from . import db_operations as db

def is_admin(user):
    """Check if the user is a superuser (Admin)."""
    return user.is_superuser

from django.contrib.auth.models import User

def signup_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            user_type = data.get('user_type', 'staff')
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)
            
            is_admin_user = (user_type == 'admin')
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                is_superuser=is_admin_user,
                is_staff=(user_type != 'member') # Only staff/admin can access management views
            )
            
            # If user is a member, link to Member table using their email
            if user_type == 'member':
                db.add_member_to_db({
                    'Name': username.title(),
                    'Email': email,
                    'Phone': 'N/A',
                    'Address': 'Registered Online'
                })
            
            login(request, user)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return render(request, 'signup.html')

@login_required
def get_my_issues(request):
    """Provide specific issue records for the logged-in student/member."""
    return JsonResponse(db.get_member_issues(request.user.email), safe=False)

def login_view(request):
    """Handle user login authentication."""
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
    return render(request, 'login.html')

def logout_view(request):
    """Log out the current user and redirect to the login page."""
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    """Render the application's primary user interface."""
    return render(request, 'index.html', {'user': request.user})

@login_required
def get_stats(request):
    """Provide summary dashboard metrics as a JSON response."""
    return JsonResponse(db.get_stats_from_db())

@login_required
def get_books(request):
    """Provide a comprehensive list of books with full relational details."""
    return JsonResponse(db.get_all_books_with_details(), safe=False)

@login_required
def get_members(request):
    """Provide a complete list of registered library members."""
    return JsonResponse(db.get_all_members_from_db(), safe=False)

@login_required
def get_recent_issues(request):
    """Provide the five most recent issue records for dashboard display."""
    return JsonResponse(db.get_recent_issues_for_dashboard(), safe=False)

@login_required
def get_all_issues(request):
    """Provide every issue record with detailed member and staff associations."""
    return JsonResponse(db.get_all_issues_with_details(), safe=False)

@login_required
def get_staff(request):
    """Provide a complete list of library staff members."""
    return JsonResponse(db.get_all_staff_from_db(), safe=False)

@login_required
def get_ratings(request):
    """Provide a collection of book ratings and corresponding reviews."""
    return JsonResponse(db.get_all_ratings_from_db(), safe=False)

@login_required
def get_categories(request):
    """Provide a list of all book categories for form selection."""
    return JsonResponse(db.get_all_categories(), safe=False)

@csrf_exempt
@login_required
def add_book(request):
    """Process a request to insert a new book record into the system."""
    if request.method == 'POST':
        try:
            db.add_book_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
def add_member(request):
    """Process a request to register a new system member."""
    if request.method == 'POST':
        try:
            db.add_member_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
def add_issue(request):
    """Process a request to register a new book issue event."""
    if request.method == 'POST':
        try:
            db.add_issue_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def add_staff(request):
    """Process a request to add a new staff member (Admin only)."""
    if request.method == 'POST':
        try:
            db.add_staff_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
def complete_issue(request, issue_id):
    """Handle marking an issue as completed."""
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    try:
        db.complete_issue_in_db(issue_id)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    """Handle the removal of a specific book record (Admin only)."""
    db.delete_item_from_db('Book', 'BookID', book_id)
    return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_member(request, member_id):
    """Handle the removal of a specific member record (Admin only)."""
    db.delete_item_from_db('Member', 'MemberID', member_id)
    return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_issue(request, issue_id):
    """Handle the removal of a specific issue record (Admin only)."""
    db.delete_item_from_db('Issue', 'IssueID', issue_id)
    return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_staff(request, staff_id):
    """Handle the removal of a specific staff record (Admin only)."""
    db.delete_item_from_db('Staff', 'StaffID', staff_id)
    return JsonResponse({'status': 'success'})
