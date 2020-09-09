<?php 

$conn = mysqli_connect("localhost","root","","raport");
if(!$conn)
{	echo mysqli_stmt_error($conn);
	exit();
}
else
{
	$stmt = mysqli_stmt_init($conn);
	$query = 'SELECT ID,Store_name, Store_category FROM STORE LIMIT 400';
	$stmt->prepare($query);
	$stmt->execute();
	$result = $stmt->get_result();
	$jsont = '
	{
		"nodes": [
				';
	foreach($result as $data)
	{
		$id = $data['ID'];
		$category = $data["Store_category"];
		$store = $data["Store_name"];
		
		$jsont .=  '{'.PHP_EOL.
						'	"Category":"'.$category.'",
		"id":'.$id.',
		"store":"'.$store.'"'.PHP_EOL.'},'.PHP_EOL;
	}
	$jsont .= '
			],
			"links": [
	';
	$query = 'SELECT ID,Store_name, Store_category FROM STORE LIMIT 400';
	$stmt->prepare($query);
	$stmt->execute();
	$result = $stmt->get_result();
	$next = 0;
	foreach($result as $cat)
	{
		$next = rand(1,20);
		$id = $cat['ID'];
		#$next = (int)$id -1;
		#if($next === 0)
		#{
		#	$next =	1;
		#}
		$category = $cat["Store_category"];
		
		$store = $cat["Store_name"];
		$jsont .= '
		{
			"source": '.$id.',
			"target": '.$next.',
			"weight": 1
		},
	';
	}
	$jsont .= '
	]
	
}
	';
	$fp = fopen('../export.json','a');
	fwrite($fp,$jsont);
	

}







?>
