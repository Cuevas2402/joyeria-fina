
$(document).ready(() => {
    $('#detalles').click(function(){
        var id = $(this).val();

        window.location.href = 'http://127.0.0.1:5000/vehicles/detailes/'+id;
    });
});

$(document).ready(() => {
    $('#editar').click(function(){
        var id = $(this).val();

        window.location.href = 'http://127.0.0.1:5000/vehicles/edit/'+id;
    });
});