<?php

  include 'config.php';

  // get JSON input from HTTP POST
  $postdata = file_get_contents("php://input");

  // JSON Decode from input
  $request = json_decode($postdata, true);

  $array = array();
  foreach ($request as $key) {
    // echo $key['value'].'<br />';
    $tanaman = $key['tanaman'];
    // echo $tanaman;

    $disease = $key['disease'];
    // echo $disease;

    // $index = $key['index'];
    $query = mysqli_query($link, "SELECT * FROM `all_view` where nama_latin = '$tanaman' and disease_name = '$disease'");

    $array1 = array();
    $array2 = array();
    $array3 = array();

    // if (count($array1) == 0) echo 'kosong';

    // $array1[] = array('nama_latin' => 'ccc', 'nama' => 'ddd');
    //
    // // print_r($array1);
    //
    // foreach ($array1 as $arr) {
    //   if ($arr['nama_latin'] == 'aaa' && $arr['nama'] == 'bbb') echo 'hooray';
    // }

    while($row = mysqli_fetch_assoc($query)){
      // $array[] = array(id => $index, plant => $value, cid => $row['cid'], compound => $row['nama']);
      // $array[] = array($value.' (Protein)', $row['disease_name'].' (Disease)', 2);

      $cek1 = false;
      if (count($array1) == 0) {
        $array1[] = array('nama_latin' => $row['nama_latin'], 'nama' => $row['nama']);
        $array[] = array($row['nama_latin'].' (Plant)', $row['nama'].' (Compound)', 1);
      }
      foreach ($array1 as $arr1) {
        echo $nama;
        if ($arr1['nama_latin'] == $row['nama_latin'] && $arr1['nama'] == $row['nama']) $cek1 = true;
        else {
          $array1[] = array('nama_latin' => $row['nama_latin'], 'nama' => $row['nama']);
        }
      }

      if (!$cek1 && count($array1) != 0) {
        $array[] = array($row['nama_latin'].' (Plant)', $row['nama'].' (Compound)', 1);
      }
      $cek1 = false;

      $cek2 = false;
      if (count($array2) == 0){
        $array2[] = array('nama' => $row['nama'], 'protein_name' => $row['protein_name']);
        $array[] = array($row['nama'].' (Compound)', $row['protein_name'].' (Protein)', rand(1,1000)/1000);
      }
      foreach ($array2 as $arr2) {
        if ($arr2['nama'] == $row['nama'] && $arr2['protein_name'] == $row['protein_name']) $cek2 = true;
        else {
          $array2[] = array('nama' => $row['nama'], 'protein_name' => $row['protein_name']);
        }
      }

      if (!$cek2 && count($array2) != 0) {
        $array[] = array($row['nama'].' (Compound)', $row['protein_name'].' (Protein)', rand(1,1000)/1000);
      }
      $cek2 = false;

      $cek3 = false;
      if (count($array3) == 0){
        $array3[] = array('protein_name' => $row['protein_name'], 'disease_name' => $row['disease_name']);
        $array[] = array($row['protein_name'].' (Protein)', $row['disease_name'].' (Disease)', 1);
      }
      foreach ($array3 as $arr3) {
        if ($arr3['protein_name'] == $row['protein_name'] && $arr3['disease_name'] == $row['disease_name']) $cek3 = true;
        else {
          $array3[] = array('protein_name' => $row['protein_name'], 'disease_name' => $row['disease_name']);
        }
      }

      if (!$cek3 && count($array3) != 0) {
        $array[] = array($row['protein_name'].' (Protein)', $row['disease_name'].' (Disease)', 1);
      }
      $cek3 = false;

      // $cek3 = false;
      // if (count($array3) == 0) {
      //   $array3[] = array('protein_name' => $row['protein_name'], 'disease_name' => $row['disease_name']);
      //   $array[] = array($row['protein_name'].' (Protein)', $row['disease_name'].' (Disease)', 1);
      // }
      // foreach ($array3 as $arr3) {
      //   if ($arr3['protein_name'] == $row['protein_name'] && $arr3['disease_name'] == $row['disease_name']) $cek3 = true;
      //   else {
      //     $array3[] = array('protein_name' => $row['protein_name'], 'disease_name' => $row['disease_name']);
      //   }
      // }
      //
      // if (!$cek3 && count($array3) != 0) {
      //   $array[] = array($row['protein_name'].' (Protein)', $row['disease_name'].' (Disease)', 1);
      // }
      // $cek3 = false;


      // $array[] = array($row['nama_latin'].' (Plant)', $row['nama'].' (Compound)', 1);
      // $array[] = array($row['nama'].' (Compound)', $row['protein_name'].' (Protein)', rand(1,1000)/1000);
      // $array[] = array($row['protein_name'].' (Protein)', $row['disease_name'].' (Disease)', 1);
    }
  }
  //
  header('Content-type: application/json');
  // $array = array_map("unserialize", array_unique(array_map("serialize", $array)));

  echo json_encode($array);

//   $a1=array("Dog","Cat");
// $a2=array("Puppy","Kitten");
// print_r(array_map(null,$a1,$a2));

  // $array = json_decode($array, true);
  //
  // print_r($array);

?>
