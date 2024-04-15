function generateHeader() {
    const header = `
    <!-- Header -->
    <header class="bg-custom text-custom" style="border-bottom: 0.5px solid black;">
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-12 mb-md-0 mb-2 text-center text-md-left">
                    <a href="/dashboard">
                        <button class="btn border-0 btn-custom text-custom">Fins-Fintech</button>
                    </a>
                </div>
                <!-- Black line for small screens -->
                <div class="col-12 text-center d-md-none">
                    <hr style="background-color: black;">
                </div>
                <div class="col-md-6 col-12 mb-md-0 mb-2 text-center text-md-right">
                    <div class="btn-group">
                        <button class="btn border-0 btn-custom text-custom dropdown-toggle" type="button" id="userDropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
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
    <script>
        var timeout;

        function resetTimer() {
            clearTimeout(timeout);
            timeout = setTimeout(logout, 600000); // 10 minutes in milliseconds
        }

        function logout(){
            window.location.href = '/logout'; // Redirect to logout route
            alert("You have been logged out due to inactivity");
        }

        document.onmousemove = resetTimer; // Reset timer on mouse movement
        document.onkeypress = resetTimer; // Reset timer on keypress

        resetTimer(); // Initial call to start the timer


    </script>
    `;
    document.write(header);
}