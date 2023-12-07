<?php require_once("../includes/head.php")?>
<?php require_once("../includes/nav.php")?>
<head>
<link rel="stylesheet" href="../static/bootstrap.css">
</head>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="index.php">Login and Registration System</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="index.php">Home <span class="sr-only">(current)</span></a>
                </li>
                </ul>
                <?php
                    if(isset($_SESSION['admin'])){
                        //echo "hidsoinfonsdkfsdkf";
                ?>
                    <a href="admin.php"><button class="btn btn-dark mr-1">Admin Page</button></a>
                <?php
                    }
                
                    if(isset($_SESSION['Email']) || isset($_COOKIE['email']))
                    //if(true)
                    {
                ?>
                    <a href="requestEvaluation.php"><button class="btn btn-dark mr-1">Request Evaluation</button></a>
                    <a href="logout.php" ><button class="btn btn-dark mr-1">Logout</button></a>
                <?php
                    }
                    else
                    {
                ?>
                
                <a href="login.php"><button class="btn btn-dark mr-1">Login</button></a>
                    <a href="register.php"><button class="btn btn-dark">Register </button></a>
                <?php
                    }
                ?>
        </div>
    </nav>
    
<h1 style="color: red  ">This is a title  ... or is it! </h1>
    
<?php require_once("../includes/footer.php")?>