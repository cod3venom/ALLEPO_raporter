<?php 

    $conn = mysqli_connect('localhost','root','','Raporter');
    if(!$conn)
    {
        mysqli_errno($conn);
        exit();
    }

?>