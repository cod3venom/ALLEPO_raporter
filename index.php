<?php 

     

     
    class DB
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
        function Exists($column,$table,$value)
        {
            require 'conn.php';
            $stmt = $this->STMT($conn,'SELECT '.$column.' FROM '.$table.' WHERE '.$column.' = ?');
            $stmt->execute(); $stmt->bind_param("s",$value);
            if($this->Count($stmt) > 0)
            {
                return TRUE;
            }
            return FALSE;
        } 
    }
    class Storage extends DB
    {
        public function Random()
        {
            require 'conn.php';
            $stmt = $this->STMT($conn,'SELECT USERAGENT FROM AGENTS ORDER BY RAND() LIMIT 1');
            $stmt->execute(); $result = $stmt->get_result();
            foreach($result as $agent)
            {
                return $agent['USERAGENT'];
            }
        }
         
        public function Write_store($store,$category)
        {
            require 'conn.php';
            if(!$this->Exists('Store_name','STORE',$store))
            {
                $stmt = $this->STMT($conn,"INSERT INTO STORE(Store_name, Store_category) VALUES (?,?)");
                $stmt->bind_param("ss",$store,$category);
                if($this->Store($stmt)>0)
                {
                    echo 'Added';
                }
                else
                {
                    echo 'some error';
                }
            }
            else
            {
                echo 'duplicate';
            }
        }
        public function Write_page($category,$link)
        {
            require 'conn.php';
            if(!$this->Exists('PAGE_LINK','PAGES',$link))
            {
                $stmt = $this->STMT($conn,"INSERT INTO PAGES(PAGE_CATEGORY,PAGE_LINK) VALUES (?, ?)");
                $stmt->bind_param("ss",$category,$link);
                if($this->Store($stmt)>0)
                {
                    echo 'Added';
                }
                else
                {
                    echo 'some error';
                }
            }
            else
            {
                echo 'duplicate';
            }
        }
    }
    if(isset($_POST['random']))
    {
        $storage = new Storage();
        echo $storage->Random();
    }
    if(isset($_POST['write_store']) && isset($_POST['category']))
    {
        $store = $_POST['write_store'];
        $category = $_POST['category'];

        $storage = new Storage();
        $storage->Write_store($store,$category);
    }
    if(isset($_POST['write_page']) && isset($_POST['category']) && isset($_POST['link']))
    {
        $category = $_POST['category'];
        $link = $_POST['link'];
        $storage = new Storage();
        $storage->Write_page($category,$link);
    }

?>