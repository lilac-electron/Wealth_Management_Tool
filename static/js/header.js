function generateHeader() {
    const header = `
    <!-- Header -->
    <header class="bg-ddanger text-white p-3">
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-12 mb-md-0 mb-2 text-center text-md-left">
                    <a href="/dashboard">
                        <button class="btn btn-light border-0 bg-dark text-white">Fins-Fintech</button>
                    </a>
                </div>
                <div class="col-md-6 col-12 mb-md-0 mb-2 text-center text-md-right">
                    <div class="btn-group">
                        <button class="btn btn-light border-0 bg-dark text-white dropdown-toggle" type="button" id="userDropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Welcome, ${name}
                        </button>
                        <div class="dropdown-menu" aria-labelledby="userDropdown">
                            <!-- Add your dropdown options here -->
                            <a class="dropdown-item" href="#">Change Email</a>
                            <a class="dropdown-item" href="#">Personal Infomation</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="/logout">Logout</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>
    `;
    document.write(header);
}