$(document).ready(function() {
    $('#dataTable').DataTable();
  });

  $(document).ready(function() {
    $('#productTable').DataTable( {
      "order": [[ 3, "desc" ]],
      scrollY:'50vh',
      scrollCollapse: true,
      paging: false
  } );
});
  
  