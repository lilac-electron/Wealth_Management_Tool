function generateNavbar(currentPage="") {
    const navbar = `
    <link rel="stylesheet" href="{{ url_for('static', filename='css/newStyle.css') }}">
    <nav class="navbar navbar-expand-md bg-custom text-custom">
        <div class="container">

            <!-- Navbar Toggler Button for Small Screens -->
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon">Navbar Toggle Button</span>
            </button>

            <!-- Navbar Links with Invisible Boxes -->
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mx-auto">
                    <li class="nav-item">
                        <a class="nav-link border-0 btn-custom text-custom mr-2 ${currentPage === '/credits' ? 'active' : ''}" href="/credits">Current Credits</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 btn-custom text-custom mr-2 ${currentPage === '/assetValue' ? 'active' : ''}" href="/assetValue">Current Asset Value</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 btn-custom text-custom mr-2 ${currentPage === '/simulatedGrowth' ? 'active' : ''}" href="/simulatedGrowth">Simulated Growth</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 btn-custom text-custom mr-2 ${currentPage === '/transactions' ? 'active' : ''}" href="/transactions">Track Transactions</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 btn-custom text-custom mr-2 ${currentPage === '/tools' ? 'active' : ''}" href="/tools">Finance Tools</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 btn-custom text-custom mr-2 ${currentPage === '/feedbackForm' ? 'active' : ''}" href="/feedbackForm">Feedback Form</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    `;
    document.write(navbar);
}

// Example: Call generateNavbar function and pass the current page URL
//generateNavbar('/credits');
