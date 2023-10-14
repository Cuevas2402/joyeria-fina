$(document).ready(() =>{
    $('#branches').on('change', function(){
        var id = $(this).val();
        $.ajax({
            url:'http://127.0.0.1:5000/get-companies',
            type: 'POST', 
            data : {
                'id':id
            },
            success: (data) =>{
                $('#company').empty();
                $('#vehicle').empty();

                $('#company').append($('<option>', {
                    value: '',
                    text: '-- Selecciona una Compañía --'
                }));

                $('#vehicle').append($('<option>', {
                    value: '',
                    text: '-- Selecciona un Vehiculo --'
                }));

                $.each(data.nearest_companies, function (index, company) {
                    $('#company').append($('<option>', {
                        value: company.company_id, 
                        text: company.company_id + " - " + company.company_name 
                    }));
                });
            }
        });
    });
});

$(document).ready(() =>{
    $('#company').on('change', function(){
        var id = $(this).val();
        $.ajax({
            url:'http://127.0.0.1:5000/get-vehicles',
            type: 'POST', 
            data : {
                'id':id
            },
            success: (data) =>{
                $('#vehicle').empty();

                $('#vehicle').append($('<option>', {
                    value: '',
                    text: '-- Selecciona un Vehiculo --'
                }));

                $.each(data, function(index, vehicle) {
                    console.log(vehicle)
                    $('#vehicle').append($('<option>', {
                        value: vehicle[0],
                        text: vehicle[0] + " " + vehicle[1]
                    }));
                });
            }
        });
    });
});