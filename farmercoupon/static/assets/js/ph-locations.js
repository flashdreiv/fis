$(document).ready(function () {
  $("#id_region").change(function () {
    const regionId = $(this).val();
    let url_api_endpoint = "/api/location/provinces";

    $.ajax({
      method: "POST",
      url: url_api_endpoint,
      data: {
        id_region: regionId,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (data) {
        let html_data = '<option value="">Select Province</option>';
        data.forEach(function (province) {
          html_data += `<option value="${province.id}">${province.name}</option>`;
        });
        $("#id_province").html(html_data); // Corrected selector
        $("#id_city").html('<option value="">Select City</option>'); // Reset city
        $("#id_barangay").html('<option value="">Select Barangay</option>'); // Reset barangay
      },
    });
  });

  $("#id_province").change(function () {
    const provinceId = $(this).val();
    let url_api_endpoint = "/api/location/cities";

    $.ajax({
      method: "POST",
      url: url_api_endpoint,
      data: {
        id_province: provinceId,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (data) {
        let html_data = '<option value="">Select City</option>';
        data.forEach(function (city) {
          html_data += `<option value="${city.id}">${city.name}</option>`;
        });
        $("#id_city").html(html_data); // Corrected selector
        $("#id_barangay").html('<option value="">Select Barangay</option>'); // Reset barangay
      },
    });
  });

  $("#id_city").change(function () {
    const cityId = $(this).val();
    let url_api_endpoint = "/api/location/barangays";

    $.ajax({
      method: "POST",
      url: url_api_endpoint,
      data: {
        id_city: cityId,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (data) {
        let html_data = '<option value="">Select Barangay</option>';
        data.forEach(function (barangay) {
          html_data += `<option value="${barangay.id}">${barangay.name}</option>`;
        });
        $("#id_barangay").html(html_data);
      },
    });
  });
});
