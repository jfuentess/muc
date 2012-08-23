<html>
	<head>

		<style type="text/css">
			table {
				width: 90%;
				padding-left: 5%;
			}

			td {
				text-align: center;
			}

			td#logo1 {
				width: 10%;
			}

			td#form {
				width: 80%;
			}

			td#logo2 {
				width: 10%;
			}

			img#diicc {
				width: 85%;
			}

			img#udec {
				width: 85%;
			}

			.top {
				text-align: center;
			}
			.down {
				padding-top: 6%;
			}

			body.vector-animateLayout #mw-panel {
				-moz-transition: padding-left 250ms ease 0s;
				padding-top: 22%;
			}			

			body.vector-animateLayout #left-navigation {
				padding-top: 22%;
			}

			body.vector-animateLayout #p-logo {
				padding-top: 175%;
			}

			div#mw-head {
				padding-top: 22%;
			}

			body.vector-animateLayout #p-personal {
				padding-top: 22%;
			}
		  </style>

		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<link rel="shortcut icon" href="./favicon.ico" />
		<title>¡Viva la Ingeniería! - DIICC</title>
	
	</head>
	<body>
		<div class="top">
			<table>
				<tr>
					<td id="logo1">
						<img id="diicc" src="./diicc.png" />
					</td>
					<td id="form">
						<h1>Verbalizaci&oacute;n de expresiones matem&aacute;ticas</h1>
						<h3>Desde p&aacute;ginas de Wikipedia</h3>

						<form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="get">
							Ingresa URL: <input type="text" name="url" size=90% /><br/><br/>
							<input type="submit" name="submit" value="Submit" />
						</form>
					</td>
					<td id="logo2">
						<img id="udec" src="./UdeC.png" />
					</td>
				</tr>
			</table>
		</div>

		<div class="down">
			<?php

			$server = $_SERVER["SERVER_NAME"];
			$port = $_SERVER["SERVER_PORT"];
			$page = $_SERVER["PHP_SELF"];

			if(isset($_GET['url']))
			{	
				exec('python reader.py "'.$_GET['url'].'" '.$server." ".$port." ".$page, $salida);

				foreach($salida as $linea)
				{
					echo $linea;
				}
			}
			?>
		</div>
	</body>
</html>
