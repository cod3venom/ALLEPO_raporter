<?php 

    $conn = mysqli_connect("localhost","root","","raport");
    if(!$conn)
    {	echo mysqli_stmt_error($conn);
        exit();
    }


?>