$( "#add_purchase_button" ).click(function() {
    var name = $("#name").val();
            var markup = "<tr><td></td></tr>";
            $("table tbody").append(markup);
});
