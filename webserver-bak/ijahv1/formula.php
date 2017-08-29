<!DOCTYPE html>
<html>
<head>


<link href="library_bootstrap/css/bootstrap-responsive.css" rel="stylesheet" type="text/css"/>

<script>

	function setProgress(percent,bar,progress)
	{
		// Jika diatas 0 % memberikan efek loading berwarna biru 
		// Jika diatas 50 % memberikan efek loading berwarna kuning 
		// Jika diatas 51 % memberikan efek loading berwarna hijau 
		bar.style.width = percent + "%";
		if (percent > 90)
			bar.className = "bar bar-success"; // "bar bar-success" dan "bar bar-success" standart yang telah diberikan twitter bootstrap
		else if (percent > 50)
			bar.className = "bar bar-warning";
	}
	
	// Menghapus evek loading
	function clear_loading()
	{
		$('#background_loading').fadeOut('slow',function(){
			$('#proses_loading').fadeOut('slow');
			$('#proses_loading').remove();
			$(this).remove();
		});
	}
	
	$(function()
	{
		// ketika Click Button Loading maka akan meberikan efek transparan yang akan disisipkan kedalam akhir tag body
		$('#do_loading').click(function()
		{
			var str = '<div id="background_loading" style="display:none;background: #FFF;opacity: 0.7;width: 100%; height:1000px; top: 0;bottom: 0;left: 0%;z-index: 1100;position: absolute;"></div>'
			str += '<div id="proses_loading" class="progress progress-striped active" style="display:none;position: fixed;z-index: 1200;top: 40%;left: 40%;width: 300px;"><div id="myProgress" class="bar" style="width: 0%;"></div></div>';
			$('body').append(str);
			
			// memberikan evek Fade Out 
			$('#background_loading').fadeOut('slow',function()
			{
				$('#proses_loading').fadeOut('slow');
				$(this).fadeIn('slow',function()
				{
					$('#proses_loading').fadeIn('slow');
					var bar = document.getElementById("myProgress");
					var progress = 0;
					var interval = setInterval(
						function()
						{
							// funsi setProgress ini lah yang akan memberikan perhitungan 1 - 100 %
							setProgress(++progress,bar,progress);
							
							if (progress == 100)
							{
								window.clearInterval(interval);
								clear_loading();
							}
						}, 30);
				});
			});
		});
	});
</script>
</head>
<body><br />
<font size="+2" face="Arial, Helvetica, sans-serif" color="#666666"><b>Menu Formula&nbsp; > &nbsp;Racik Formula</b></font>
<form action="proses.php" method="post" class="boxformula">
	<?php
	
	for ($i=0;$i<$jumlahformula;$i++){
	echo '<div><label align="left" for="Formula-',$i,'" ><font color="#FFFFFF" size="+1"><b>Formula ',$i+1,'</b></font></label></div>',
		 '<select id="tanaman1-',$i,'" name="tanaman1-',$i,'" placeholder="Pilih Tanaman Analgesic..." style="width:220px" required>',tanaman1(),'</select>',
		 '<select id="tanaman2-',$i,'" name="tanaman2-',$i,'" placeholder="Pilih Tanaman Antibacterial..." style="width:220px" required>',tanaman2(),'</select>',
		 '<select id="tanaman3-',$i,'" name="tanaman3-',$i,'" placeholder="Pilih Tanaman Antiinflammatory..." style="width:240px" required>',tanaman3(),'</select>',
		 '<select id="aktifitas-',$i,'" name="aktifitas-',$i,'" placeholder="Pilih Aktivitas..." style="width:200px" required>',activity($efficacy),'</select>',
		 '<select id="tanaman4-',$i,'" name="tanaman4-',$i,'" placeholder="Pilih Tanaman" style="width:200px" required></select><br/><br />';
	}
	?>	
	<div class="alert alert-info" style="width:1030px">
                Semua Formula harus diisi sebelum melanjutkan proses
    </div>
    <font color="#FFFFFF" size="+1"><b>Pilih Metode</b></font><br>
    <input type="checkbox" name="check_list[]" alt="Checkbox" value="1"><font color="#FFFFFF" size="+1">PLS-DA &nbsp;&nbsp;&nbsp;</font>
    <input type="checkbox" name="check_list[]" alt="Checkbox" value="2"><font color="#FFFFFF" size="+1">Multiway PLS &nbsp;&nbsp;&nbsp;</font>
    
    <input type="checkbox" name="check_list[]" alt="Checkbox" value="3"><font color="#FFFFFF" size="+1">Support Vector Machine &nbsp;&nbsp;&nbsp;</font>
    
    <input type="checkbox" name="check_list[]" alt="Checkbox" value="4"><font color="#FFFFFF" size="+1">VFI5</font>
 <br><br>
	<input type="hidden" name="jumlahformula" value="<?php echo $jumlahformula; ?>">
	<input type="hidden" name="efficacy" value="<?php echo $efficacy; ?>">
	<button id="do_loading" class="btn btn-success" type="submit" value="proses">Proses</button>
	<!--<input type="submit" class="btn" value="proses">-->
	</form>
<script>
	$('select#efficacy').selectize();
	$(function () { $("input,select,textarea").not("[type=submit]").jqBootstrapValidation(); } );
<?php
	for ($i=0;$i<$jumlahformula;$i++){
		echo '$("select#tanaman1-',$i,'").selectize();',
			 '$("select#tanaman2-',$i,'").selectize();',
			 '$("select#tanaman3-',$i,'").selectize();';					
		} 
	for ($i=0;$i<$jumlahformula;$i++){
		echo 	'var aktifitas_',$i,', $aktifitas_',$i,';',
				'var tanaman4_',$i,', $tanaman4_',$i,';',
				'$aktifitas_',$i,' = $("#aktifitas-',$i,'").selectize({',
					'onChange: function(id) {
						if (!id.length) return;',
						'tanaman4_',$i,'.disable();',
						'tanaman4_',$i,'.clearOptions();',
						'tanaman4_',$i,'.load(function(callback) {',
						'tanaman4_',$i,'.enable();
						callback(tanamanfull[id]);',
							'});
						}
					});',
				'$tanaman4_',$i,' = $("#tanaman4-',$i,'").selectize({
						valueField: "id",
						labelField: "nama",
						searchField: ["nama"]
					});',
				'aktifitas_',$i,'  = $aktifitas_',$i,'[0].selectize;',
				'tanaman4_',$i,' = $tanaman4_',$i,'[0].selectize;',
				'tanaman4_',$i,'.disable();';
		}
?>
	</script>
	</body>
</html>