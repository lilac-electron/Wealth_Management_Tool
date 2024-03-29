function generateNavbar(currentPage="") {
    const navbar = `
    <style>
        .nav-link:hover {
            border-radius: 10px;
        }
        .active {
            color: #333; /* Adjust text color accordingly */
        }
        input[type=number]::-webkit-inner-spin-button,
        input[type=number]::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        input[type=number] {
            -moz-appearance: textfield;
        }
    </style>
    <nav class="navbar navbar-expand-md navbar-light bg-light">
        <div class="container">

            <!-- Navbar Toggler Button for Small Screens -->
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Navbar Links with Invisible Boxes -->
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mx-auto">
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2 ${currentPage === '/credits' ? 'active' : ''}" href="/credits">Current Credits</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2 ${currentPage === '/assetValue' ? 'active' : ''}" href="/assetValue">Current Asset Value</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2 ${currentPage === '/simulatedGrowth' ? 'active' : ''}" href="/simulatedGrowth">Simulated Growth</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2 ${currentPage === '/transactions' ? 'active' : ''}" href="/transactions">Track Transactions</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2 ${currentPage === '/tools' ? 'active' : ''}" href="/tools">Finance Tools</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2 ${currentPage === '/feedbackForm' ? 'active' : ''}" href="/feedbackForm">Feedback Form</a>
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
