function generateNavbar() {
    const navbar = `
    <style>
        .nav-link:hover {
            border-radius: 10px;
        }
    </style>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">

            <!-- Navbar Toggler Button for Small Screens -->
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Navbar Links with Invisible Boxes -->
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mx-auto">
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2" href="/credits">Current Credits</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2" href="/assetValue">Current Asset Value</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2" href="/simulatedGrowth">Simulated Growth</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2" href="/transactions">Track Transactions</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link border-0 bg-light mr-2" href="/updateFinances">Update Financial Info</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    `;
    document.write(navbar);
}

generateNavbar();