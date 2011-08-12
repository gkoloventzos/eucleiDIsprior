<?php
$url = explode("/", $_SERVER["REQUEST_URI"]);
$sure_file = $url[sizeof($url)-1];
$file_name = explode(".", $sure_file);
$class = $file_name[sizeof($file_name)-2];
$file_name[sizeof($file_name)-1] = "txt";
$read_file = implode(".",$file_name);
$fp = fopen($read_file, "r");
$theData = fread($fp, filesize($read_file));
$regexp = "<a name=\"([^\"]*)\"><\/a>";
echo "<div id=\"scrollingDiv\">\n<h3>Sort-cut</h3>\n<ul class=\"sidemenu\">\n";
preg_match_all("/$regexp/siU",$theData,$matches);
foreach($matches[1] as $match) { 
	if (strcmp($match,"definition") == 0){
		echo "<li><a href=\"#definition\">Home</a></li>";
	}
	else{
		$Match = ucfirst($match);
		echo "<li><a href=\"#$match\">$Match</a></li>";
	}
}
echo "<li><a href=\"./examples$class.php\">Examples</a></li>";
echo "</ul>\n</div>\n";
?>
