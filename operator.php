<?php 
    require_once "Core/functions.php";
    $set = new Dataset();
    if(isset($_POST['c_t']))
    {
        echo $set->Categories_total();
    }
    if(isset($_POST['s_t']))
    {
        echo $set->Stores_total();
    }
    if(isset($_POST['p_t']))
    {
        echo $set->Pages_total();
    }

?>