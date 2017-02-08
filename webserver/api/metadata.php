<?php
  include 'config.php';

  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $cond = '';
  $table = 'ERROR_UNKNOWN_TABLE_PLEASE_FIX';
  $col = 'ERROR_UNKNOWN_COL_PLEASE_FIX';
  $selectAll = false;
  foreach($requestList as $req) {
    if (isset($req['id'])) {
      $val = $req['id'];

      $id = '';
      if (strpos($val, 'PLA') !== false) {
        $id = 'pla_id';
        $table = 'plant';
        $col = 'pla_id,pla_name,pla_idr_name';
      }
      elseif (strpos($val, 'COM') !== false) {
        $id = 'com_id';
        $table = 'compound';
        $col = 'com_id,com_cas_id,com_drugbank_id,com_knapsack_id,com_kegg_id,com_pubchem_id,com_inchikey,com_smiles';
      }
      elseif (strpos($val, 'PRO') !== false) {
        $id = 'pro_id';
        $table = 'protein';
        $col = 'pro_id,pro_name,pro_uniprot_id,pro_uniprot_abbrv,pro_pdb_id';
      }
      elseif (strpos($val, 'DIS') !== false) {
        $id = 'dis_id';
        $table = 'disease';
        $col = 'dis_id,dis_omim_id,dis_name,dis_uniprot_abbrv';
      }

      if (strpos($val,'ALL_ROWS')!==false) {
        $selectAll = true;
        break;
      }
      $cond = $cond.$id."="."'".$val."'".' OR ';
    }
  }

  $cond = substr($cond,0,-4);// remove the last OR
  $query = "SELECT ".$col." FROM ".$table;
  if ($selectAll===false) {
    $query = $query." WHERE ".$cond;
  }

  $resp = pg_query($link, $query);
  $respArr = array();
  while($row = pg_fetch_assoc($resp)){
    $respArr[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($respArr);
?>
