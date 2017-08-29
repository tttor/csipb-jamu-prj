<!DOCTYPE HTML>
<html>
<head>
<title>Registration</title>
<meta charset="UTF-8" />
<meta name="Designer" content="PremiumPixels.com">
<meta name="Author" content="$hekh@r d-Ziner, CSSJUNTION.com">
<link rel="stylesheet" type="text/css" href="css/reset.css">
<link rel="stylesheet" type="text/css" href="css/register.css">
</head>
<body>
<form class="box login" action="login/submit.php" method="post">
	<fieldset class="boxBody">
	<center>
<img src="images/logo.png" height="90px"></center>
	  <label>Username</label>
	  <input type="text" name="username" id="username" size="50" tabindex="1" required placeholder="username"/>
	  <label>Email</label>
	  <input type="text" name="email" id="email" required placeholder="Your True Email" />
	  <label>Password</label>
	  <input type="password"  name="pass1" id="password" required placeholder="Your Password" />
	  <label>Re-Type Password</label>
	  <input type="password" tabindex="2" name="pass2" id="password" required placeholder="Retype your Password" />
	  <label>Fullname</label>
	  <input type="text" name="fullname" id="fullname" required placeholder="Please type your fullname" />
	  <label>Phone Numbers</label>
	  <input type="text" name="phone" id="phone" required placeholder="Your True Number Phone" />

	</fieldset>
	<footer>
	  <label><a href="index.php" class="rLink" tabindex="5" align="left">already have account? login here</a></label>
	  <input type="submit" class="btnLogin" value="Register" tabindex="4">
	</footer>
</form>
<footer id="main">
</footer>
</body>
</html>
