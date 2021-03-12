$(document).ready(function() {
    $('#dataTable').DataTable();
  });

  $(document).ready(function() {
    $('#productTable').DataTable( {
      "order": [[ 3, "desc" ]],
  } );
});
  
  