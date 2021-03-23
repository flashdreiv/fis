$('#id_region').change(function(){
    const regionId = $(this).val()
    url_api_endpoint = '/api/location/provinces'
    $.ajax({
        method:"POST",
        url:url_api_endpoint,
        data:{
            'id_region':regionId,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            $(id_province).html(data)
            let html_data = ''
            data.forEach(function(provinces){
                html_data += `<option value="${provinces.id}">${provinces.name}</option>`
            })
            $(id_province).html(html_data)
        }
    })

})

$('#id_province').change(function(){
    const provinceId = $(this).val()
    url_api_endpoint = '/api/location/cities'
    $.ajax({
        method:"POST",
        url:url_api_endpoint,
        data:{
            'id_province':provinceId,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            $(id_city).html(data)
            let html_data = ''
            data.forEach(function(cities){
                html_data += `<option value="${cities.id}">${cities.name}</option>`
            })
            $(id_city).html(html_data)
        }
    })

})

$('#id_city').change(function(){
    const cityId = $(this).val()
    url_api_endpoint = '/api/location/barangays'
    $.ajax({
        method:"POST",
        url:url_api_endpoint,
        data:{
            'id_city':cityId,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            $(id_barangay).html(data)
            let html_data = ''
            data.forEach(function(barangays){
                html_data += `<option value="${barangays.id}">${barangays.name}</option>`
            })
            $(id_barangay).html(html_data)
        }
    })

})