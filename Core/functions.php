<?php 

    

    class Database
    {
        public function STMT($conn,$query)
        {
            if($conn&&!empty($query))
            {
                $stmt = mysqli_stmt_init($conn);
                if(!$stmt->prepare($query))
                {
                     echo mysqli_stmt_error($stmt);
                     exit();
                 }
                 $stmt->prepare($query);
                 return $stmt;
            }
        }
        function Count($stmt)
         {
             $stmt->execute();
            $stmt->store_result();
            return $stmt->num_rows();
         }
         function Store($stmt)
         {
             $stmt->execute();
            $stmt->store_result();
             if(!$stmt)
             {
                 die('prepare () failed)' . htmlspecialchars($stmt->error()));
             }
             return $stmt->store_result();
        }
        function Exists($stmt)
        {
            $result = $this->Count($stmt);
            if($result > 0)
            {
                return TRUE;
            }
            else
            {
                return FALSE;
            }
            return FALSE;
        } 
    }
    class Dataset extends Database
    {
        public function Stores_total()
        {
            require_once "conn.php";
            $stmt = $this->STMT($conn,"SELECT Store_name FROM STORE");
            return $this->Count($stmt);
        }
        public function Categories_total()
        {
            require_once "conn.php";
            $stmt = $this->STMT($conn,"SELECT CATEGORY_NAME FROM CATEGORIES");
            return $this->Count($stmt);
        }
        public function Pages_total()
        {
            require_once "conn.php";
            $stmt = $this->STMT($conn,"SELECT PAGE_LINK FROM PAGES");
            return $this->Count($stmt);
        }
    }

     

?>