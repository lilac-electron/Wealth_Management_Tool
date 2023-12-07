<?php require_once("../includes/head.php")?>
<?php require_once("../includes/nav.php")?>
<head>
<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css')}}">
</head>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="index.php">Wealth Management Tool Python</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="index.php">Home <span class="sr-only">(current)</span></a>
                </li>
                </ul>
                <a href="admin.php"><button class="btn btn-dark mr-1">Admin Page</button></a>
                <a href="newEval.php"><button class="btn btn-dark mr-1">New Eval</button></a>
        </div>
    </nav>
    
<body>
    
</body>
    
<?php require_once("../includes/footer.php")?>