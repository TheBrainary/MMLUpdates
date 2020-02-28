<html><head>
<meta charset="UTF-8">
</head>

<body style="margin: 0px;">

<?php
if (isset($_POST['Play1']))
{
exec("$(which ./home/miro/stream.sh)");
}
if (isset($_POST['CreateFolder']))
{
exec("sudo /home/miro/test.sh");
}
if (isset($_POST['Stop']))
{
exec("sudo /home/miro/testcode.sh");
}
?>

<form method="post">
<button name="Play1" class="btn">Play 1</button>&nbsp;
<button name="CreateFolder" class="btn">Create Folder</button><br><br>
<button name="Stop" class="btn">Stop</button>

</form> 

</body></html>
