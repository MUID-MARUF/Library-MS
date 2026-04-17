let currentData = { books: [], members: [], issues: [], staff: [], ratings: [] };

document.addEventListener('DOMContentLoaded', () => {
    /** Initialize theme, navigation, and core application states. */
    initTheme();
    
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.page-section');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const target = item.getAttribute('data-target');
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === target) section.classList.add('active');
            });
            loadSectionData(target);
        });
    });

    loadSectionData('dashboard');
    populateAllDropdowns();

    setupForm('add-book-form', 'book-modal', '/api/books/add/', loadAllBooks);
    setupForm('add-member-form', 'member-modal', '/api/members/add/', loadAllMembers);
    setupForm('add-issue-form', 'issue-modal', '/api/issues/add/', loadAllIssues);
    setupForm('add-staff-form', 'staff-modal', '/api/staff/add/', loadAllStaff);

    document.getElementById('dark-mode-toggle').addEventListener('click', toggleTheme);
});

function initTheme() {
    /** Apply saved user theme preference on load. */
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    /** Switch between light and dark visual themes. */
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    /** Update the toggle button icon based on the current theme. */
    const icon = document.querySelector('#dark-mode-toggle i');
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

async function populateAllDropdowns() {
    /** Concurrent fetch and population of all selection dropdowns. */
    try {
        const catRes = await fetch('/api/categories/');
        const categories = await catRes.json();
        const catDropdown = document.getElementById('category-dropdown');
        if (catDropdown) {
            catDropdown.innerHTML = '<option value="">Select a Category</option>';
            categories.forEach(c => { catDropdown.innerHTML += `<option value="${c.CategoryID}">${c.CategoryName}</option>`; });
        }

        const memRes = await fetch('/api/members/');
        const members = await memRes.json();
        const memDropdown = document.getElementById('member-dropdown');
        if (memDropdown) {
            memDropdown.innerHTML = '<option value="">Choose a Member</option>';
            members.forEach(m => { memDropdown.innerHTML += `<option value="${m.MemberID}">${m.Name}</option>`; });
        }

        const staffRes = await fetch('/api/staff/');
        const staff = await staffRes.json();
        const staffDropdown = document.getElementById('staff-dropdown');
        if (staffDropdown) {
            staffDropdown.innerHTML = '<option value="">Choose Staff Member</option>';
            staff.forEach(s => { staffDropdown.innerHTML += `<option value="${s.StaffID}">${s.StaffName} (${s.Role})</option>`; });
        }

        const bookRes = await fetch('/api/books/');
        const books = await bookRes.json();
        const bookDropdown = document.getElementById('book-dropdown');
        if (bookDropdown) {
            bookDropdown.innerHTML = '<option value="">Choose a Book</option>';
            books.forEach(b => { bookDropdown.innerHTML += `<option value="${b.BookID}">${b.Title}</option>`; });
        }

        const dateInput = document.getElementById('issue-date-input');
        if (dateInput) dateInput.value = new Date().toISOString().split('T')[0];
    } catch (e) {
        console.error("Dropdown refresh failed", e);
    }
}

function showModal(id) { 
    /** Display a specific modal and refresh its dynamic data. */
    document.getElementById(id).style.display = 'block';
    populateAllDropdowns();
}

function hideModal(id) { 
    /** Conceal a specific modal and reset visibility. */
    document.getElementById(id).style.display = 'none'; 
}

function setupForm(formId, modalId, url, callback) {
    /** Generic handler for AJAX form submissions. */
    const form = document.getElementById(formId);
    if (!form) return;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            hideModal(modalId);
            e.target.reset();
            callback();
            updateDashboardStats();
            populateAllDropdowns();
        } else {
            const err = await response.json();
            alert('Operation failed: ' + err.message);
        }
    });
}

async function loadSectionData(section) {
    /** Route section requests to specific data loader functions. */
    switch (section) {
        case 'dashboard': await updateDashboardStats(); await loadRecentIssues(); break;
        case 'books': await loadAllBooks(); break;
        case 'members': await loadAllMembers(); break;
        case 'issues': await loadAllIssues(); break;
        case 'staff': await loadAllStaff(); break;
        case 'ratings': await loadAllRatings(); break;
    }
}

async function updateDashboardStats() {
    /** Fetch and render summary metrics for the dashboard view. */
    try {
        const response = await fetch('/api/stats/');
        const data = await response.json();
        document.getElementById('total-books-count').textContent = data.total_books;
        document.getElementById('total-members-count').textContent = data.total_members;
        document.getElementById('total-issues-count').textContent = data.total_issues;
        document.getElementById('avg-rating-value').textContent = data.avg_rating.toFixed(1);
    } catch (e) {}
}

async function loadRecentIssues() {
    /** Populate the dashboard's recent activity table. */
    const response = await fetch('/api/recent-issues/');
    const issues = await response.json();
    const tbody = document.querySelector('#recent-issues-table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    issues.forEach(issue => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>#${issue.IssueID}</td><td>${issue.MemberName}</td><td>${issue.IssueDate}</td><td>${issue.ReturnDate}</td><td><span class="status-badge ${issue.FineStatus === 'Paid' ? 'status-paid' : 'status-pending'}">${issue.FineStatus}</span></td>`;
        tbody.appendChild(tr);
    });
}

async function loadAllBooks() {
    /** Fetch and render the comprehensive book inventory. */
    const response = await fetch('/api/books/');
    currentData.books = await response.json();
    const tbody = document.querySelector('#all-books-table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    currentData.books.forEach(book => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${book.BookID}</td>
            <td>${book.Title}</td>
            <td>${book.AuthorName || 'Unknown'}</td>
            <td>${book.AvailableCopies}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="viewDetails('books', ${book.BookID})"><i class="fas fa-eye"></i> Details</button>
                <button class="btn btn-danger btn-sm" onclick="deleteItem('/api/books/delete/${book.BookID}/', loadAllBooks)"><i class="fas fa-trash"></i></button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function loadAllMembers() {
    /** Fetch and render the full library membership list. */
    const response = await fetch('/api/members/');
    currentData.members = await response.json();
    const tbody = document.querySelector('#all-members-table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    currentData.members.forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${m.MemberID}</td>
            <td>${m.Name}</td>
            <td>${m.Email}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="viewDetails('members', ${m.MemberID})"><i class="fas fa-eye"></i> Details</button>
                <button class="btn btn-danger btn-sm" onclick="deleteItem('/api/members/delete/${m.MemberID}/', loadAllMembers)"><i class="fas fa-trash"></i></button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function loadAllIssues() {
    /** Fetch and render all historical book issue records. */
    const response = await fetch('/api/issues/');
    currentData.issues = await response.json();
    const tbody = document.querySelector('#all-issues-table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    currentData.issues.forEach(i => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${i.IssueID}</td>
            <td>${i.MemberName}</td>
            <td>${i.IssueDate}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="viewDetails('issues', ${i.IssueID})"><i class="fas fa-eye"></i> Details</button>
                <button class="btn btn-danger btn-sm" onclick="deleteItem('/api/issues/delete/${i.IssueID}/', loadAllIssues)"><i class="fas fa-trash"></i></button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function loadAllStaff() {
    /** Fetch and render the comprehensive staff directory. */
    const response = await fetch('/api/staff/');
    currentData.staff = await response.json();
    const tbody = document.querySelector('#all-staff-table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    currentData.staff.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${s.StaffID}</td>
            <td>${s.StaffName}</td>
            <td>${s.Role}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="viewDetails('staff', ${s.StaffID})"><i class="fas fa-eye"></i> Details</button>
                <button class="btn btn-danger btn-sm" onclick="deleteItem('/api/staff/delete/${s.StaffID}/', loadAllStaff)"><i class="fas fa-trash"></i></button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function loadAllRatings() {
    /** Fetch and render user-submitted book reviews and ratings. */
    const response = await fetch('/api/ratings/');
    currentData.ratings = await response.json();
    const tbody = document.querySelector('#all-ratings-table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    currentData.ratings.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${r.BookTitle}</td>
            <td>${r.MemberName}</td>
            <td>${'⭐'.repeat(r.RatingValue)}</td>
            <td>${r.Review}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="viewDetails('ratings', ${r.RatingID})"><i class="fas fa-eye"></i> Details</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function viewDetails(type, id) {
    /** Populate and display the global details panel for a specific record. */
    const item = currentData[type].find(x => (x.BookID || x.MemberID || x.IssueID || x.StaffID || x.RatingID) == id);
    if (!item) return;

    const titleMap = { books: 'Book Details', members: 'Member Details', issues: 'Issue Details', staff: 'Staff Details', ratings: 'Rating Details' };
    document.getElementById('details-title').textContent = titleMap[type];
    
    let html = '<div class="details-grid">';
    for (const [key, value] of Object.entries(item)) {
        html += `
            <div class="detail-item">
                <span class="detail-label">${key.replace(/([A-Z])/g, ' $1').trim()}</span>
                <span class="detail-value">${value === null ? 'N/A' : value}</span>
            </div>
        `;
    }
    html += '</div>';
    
    document.getElementById('details-body').innerHTML = html;
    showModal('details-modal');
}

async function deleteItem(url, callback) {
    /** Handle record deletion requests with confirmation. */
    if (confirm('Verify record deletion?')) {
        await fetch(url, { method: 'DELETE' });
        callback();
        updateDashboardStats();
    }
}
