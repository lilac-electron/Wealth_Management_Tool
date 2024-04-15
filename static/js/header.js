function generateHeader() {
    const header = `
    <!-- Header -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/newStyle.css') }}">
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
                            <button class="dropdown-item" onclick="changeColorMode()">Change Color Mode</button>
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

        function changeColorMode() {
            // Get the <link> element that refers to the CSS file
            var cssLink = document.querySelector("link[href='{{ url_for('static', filename='css/newStyle.css') }}']");
        
            // Check if the current color mode is light or dark
            if (cssLink.href.includes("newStyle.css")) {
                // If the current mode is light, switch to dark mode
                cssLink.href = "{{ url_for('static', filename='css/darkStyle.css') }}";
                alert("Switched to Dark Mode");
            } else {
                // If the current mode is dark, switch to light mode
                cssLink.href = "{{ url_for('static', filename='css/newStyle.css') }}";
                alert("Switched to Light Mode");
            }
        }
    </script>
    `;
    document.write(header);
}