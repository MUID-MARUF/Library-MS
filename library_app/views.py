from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import db_operations as db

def index(request):
    """Render the application's primary user interface."""
    return render(request, 'index.html')

def get_stats(request):
    """Provide summary dashboard metrics as a JSON response."""
    return JsonResponse(db.get_stats_from_db())

def get_books(request):
    """Provide a comprehensive list of books with full relational details."""
    return JsonResponse(db.get_all_books_with_details(), safe=False)

def get_members(request):
    """Provide a complete list of registered library members."""
    return JsonResponse(db.get_all_members_from_db(), safe=False)

def get_recent_issues(request):
    """Provide the five most recent issue records for dashboard display."""
    return JsonResponse(db.get_recent_issues_for_dashboard(), safe=False)

def get_all_issues(request):
    """Provide every issue record with detailed member and staff associations."""
    return JsonResponse(db.get_all_issues_with_details(), safe=False)

def get_staff(request):
    """Provide a complete list of library staff members."""
    return JsonResponse(db.get_all_staff_from_db(), safe=False)

def get_ratings(request):
    """Provide a collection of book ratings and corresponding reviews."""
    return JsonResponse(db.get_all_ratings_from_db(), safe=False)

def get_categories(request):
    """Provide a list of all book categories for form selection."""
    return JsonResponse(db.get_all_categories(), safe=False)

@csrf_exempt
def add_book(request):
    """Process a request to insert a new book record into the system."""
    if request.method == 'POST':
        try:
            db.add_book_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def add_member(request):
    """Process a request to register a new system member."""
    if request.method == 'POST':
        try:
            db.add_member_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def add_issue(request):
    """Process a request to register a new book issue event."""
    if request.method == 'POST':
        try:
            db.add_issue_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def add_staff(request):
    """Process a request to add a new staff member to the organization."""
    if request.method == 'POST':
        try:
            db.add_staff_to_db(json.loads(request.body))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def delete_book(request, book_id):
    """Handle the removal of a specific book record."""
    db.delete_item_from_db('Book', 'BookID', book_id)
    return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_member(request, member_id):
    """Handle the removal of a specific member record."""
    db.delete_item_from_db('Member', 'MemberID', member_id)
    return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_issue(request, issue_id):
    """Handle the removal of a specific issue record."""
    db.delete_item_from_db('Issue', 'IssueID', issue_id)
    return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_staff(request, staff_id):
    """Handle the removal of a specific staff record."""
    db.delete_item_from_db('Staff', 'StaffID', staff_id)
    return JsonResponse({'status': 'success'})
