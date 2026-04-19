from django.db import connection

def get_stats_from_db():
    #Retrieve summary metrics for the system dashboard.
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Book")
        total_books = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Member")
        total_members = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Issue")
        total_issues = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(RatingValue) FROM Rating")
        avg_rating = cursor.fetchone()[0] or 0.0
    return {
        'total_books': total_books,
        'total_members': total_members,
        'total_issues': total_issues,
        'avg_rating': float(avg_rating)
    }

def get_all_books_with_details():
    #Fetch all books with associated author, publisher, and category information.
    query = """
        SELECT b.*, a.AuthorName, p.PublisherName, p.Address as PublisherAddress, c.CategoryName, c.Shelf_No
        FROM Book b
        LEFT JOIN Writes w ON b.BookID = w.BookID 
        LEFT JOIN Author a ON w.AuthorID = a.AuthorID
        LEFT JOIN Publish pub ON b.BookID = pub.BookID 
        LEFT JOIN Publisher p ON pub.PublisherID = p.PublisherID
        LEFT JOIN Contain con ON b.BookID = con.BookID 
        LEFT JOIN Category c ON con.CategoryID = c.CategoryID
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_all_members_from_db():
    #Fetch all registered member records.
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Member")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_all_issues_with_details():
    #Fetch all book issue records with linked member and staff details.
    query = """
        SELECT i.*, 
               m.Name as MemberName, m.Email as MemberEmail, 
               s.StaffName, s.Role as StaffRole,
               b.BookID, b.Title as BookTitle,
               a.AuthorName
        FROM Issue i
        JOIN Member m ON i.MemberID = m.MemberID
        JOIN Staff s ON i.StaffID = s.StaffID
        LEFT JOIN HasBook hb ON i.IssueID = hb.IssueID
        LEFT JOIN Book b ON hb.BookID = b.BookID
        LEFT JOIN Writes w ON b.BookID = w.BookID
        LEFT JOIN Author a ON w.AuthorID = a.AuthorID
        ORDER BY i.IssueDate DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_recent_issues_for_dashboard():
    #Fetch the five most recent issue records.
    query = """
        SELECT i.IssueID, m.Name as MemberName, i.IssueDate, i.ReturnDate, i.FineStatus
        FROM Issue i
        JOIN Member m ON i.MemberID = m.MemberID
        ORDER BY i.IssueDate DESC LIMIT 5
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_all_staff_from_db():
    #Fetch all library staff records.
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Staff")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_all_ratings_from_db():
    #Fetch all book ratings and reviews with associated titles and names.
    query = """
        SELECT r.*, b.Title as BookTitle, m.Name as MemberName
        FROM Rating r
        JOIN Book b ON r.BookID = b.BookID
        JOIN Member m ON r.MemberID = m.MemberID
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_all_categories():
    #Fetch all book categories for administrative selection.
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Category")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_member_issues(email):
    #Fetch all book issues for a specific member based on their account email.
    query = """
        SELECT i.*, b.Title as BookTitle, a.AuthorName, s.StaffName
        FROM Issue i
        JOIN Member m ON i.MemberID = m.MemberID
        JOIN HasBook hb ON i.IssueID = hb.IssueID
        JOIN Book b ON hb.BookID = b.BookID
        LEFT JOIN Writes w ON b.BookID = w.BookID
        LEFT JOIN Author a ON w.AuthorID = a.AuthorID
        JOIN Staff s ON i.StaffID = s.StaffID
        WHERE m.Email = %s
        ORDER BY i.IssueDate DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [email])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def add_book_to_db(data):
    #Insert a new book record and link associated author and category.
    with connection.cursor() as cursor:
        cursor.execute("SELECT IFNULL(MAX(BookID), 0) + 1 FROM Book")
        new_book_id = cursor.fetchone()[0]
        author_name = data.get('AuthorName')
        cursor.execute("SELECT AuthorID FROM Author WHERE AuthorName = %s", [author_name])
        author_row = cursor.fetchone()
        if author_row:
            author_id = author_row[0]
        else:
            cursor.execute("SELECT IFNULL(MAX(AuthorID), 0) + 1 FROM Author")
            author_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO Author (AuthorID, AuthorName) VALUES (%s, %s)", [author_id, author_name])
        cursor.execute("INSERT INTO Book (BookID, Title, AvailableCopies) VALUES (%s, %s, %s)",
                       [new_book_id, data['Title'], data['AvailableCopies']])
        cursor.execute("INSERT INTO Writes (BookID, AuthorID) VALUES (%s, %s)", [new_book_id, author_id])
        if data.get('CategoryID'):
            cursor.execute("INSERT INTO Contain (BookID, CategoryID) VALUES (%s, %s)", [new_book_id, data['CategoryID']])

def add_member_to_db(data):
    #Insert a new library member record.
    with connection.cursor() as cursor:
        cursor.execute("SELECT IFNULL(MAX(MemberID), 0) + 1 FROM Member")
        new_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Member (MemberID, Name, Email, Phone, Address) VALUES (%s, %s, %s, %s, %s)",
                       [new_id, data['Name'], data['Email'], data['Phone'], data['Address']])

def add_issue_to_db(data):
    #Register a new book issue and associate it with a specific book.
    with connection.cursor() as cursor:
        cursor.execute("SELECT IFNULL(MAX(IssueID), 0) + 1 FROM Issue")
        new_id = cursor.fetchone()[0]
        # Insert issue with Status 'Active'
        cursor.execute("INSERT INTO Issue (IssueID, MemberID, StaffID, IssueDate, ReturnDate, FineAmount, FineStatus, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       [new_id, data['MemberID'], data['StaffID'], data['IssueDate'], data['ReturnDate'], 0, 'No', 'Active'])
        if data.get('BookID'):
            cursor.execute("INSERT INTO HasBook (IssueID, BookID) VALUES (%s, %s)", [new_id, data['BookID']])
            # Decrement book copy count
            cursor.execute("UPDATE Book SET AvailableCopies = AvailableCopies - 1 WHERE BookID = %s", [data['BookID']])

def complete_issue_in_db(issue_id):
    #Mark an issue as 'Completed' and increment the available copies of the book.
    with connection.cursor() as cursor:
        # Get BookID for this issue
        cursor.execute("SELECT BookID FROM HasBook WHERE IssueID = %s", [issue_id])
        row = cursor.fetchone()
        if row:
            book_id = row[0]
            # Increment book copy count
            cursor.execute("UPDATE Book SET AvailableCopies = AvailableCopies + 1 WHERE BookID = %s", [book_id])
        # Update issue status
        cursor.execute("UPDATE Issue SET Status = 'Completed' WHERE IssueID = %s", [issue_id])

def add_staff_to_db(data):
    """Insert a new staff member record."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT IFNULL(MAX(StaffID), 0) + 1 FROM Staff")
        new_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Staff (StaffID, StaffName, Phone, Role) VALUES (%s, %s, %s, %s)",
                       [new_id, data['StaffName'], data['Phone'], data['Role']])

def delete_item_from_db(table_name, id_column, item_id):
    #Remove a specific record from any system table by primary key.
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", [item_id])
