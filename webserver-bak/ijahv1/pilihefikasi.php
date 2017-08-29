<br />
<font size="+2" face="Arial, Helvetica, sans-serif" color="#666666"><b>Menu Formula&nbsp; > &nbsp;Racik Formula</b></font>
<form class="boxefikasi" action="index.php" method="post">
<div align="center"><table width="100%">
<tr>
<td>
<label for="labpilef"><font color="#FFFFFF" size="+1">&nbsp;&nbsp;&nbsp;Pilih Efikasi : &nbsp;</font></label>
</td>
<td style="width:350px"><font color="#FFFFFF" size="+1"></font>
<select id="efficacy" name="efficacy" placeholder="Pilih Efikasi..." style="width:350px; z-index:-1" >
<?php efficacy(); ?>
</select>
</td>

<td>
<label for="labjumfor"><font color="#FFFFFF" size="+1">&nbsp;&nbsp;&nbsp;Banyaknya Formula : &nbsp;</font></label>
</td>
<td style="width:350px">
<select id="jumlahformula" name="jumlahformula" placeholder="Pilih Jumlah Formula..." style="width:335px" >
<?php jumlahformula(); ?>
</select>
</td>
</tr>
</table>
</div>
<br />
<button type="submit" class="btn" type="button" style="float:right; margin-right:15px">Pilih Efikasi</button>
<br>
</form>

<script>
	$('select#efficacy').selectize();
	$('select#jumlahformula').selectize();
</script>