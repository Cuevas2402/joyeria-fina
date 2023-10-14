
$(document).ready(() => {
    $('.crud-detalles').click(function(){
        var id = $(this).val();

        window.location.href = 'http://127.0.0.1:5000/vehicles/detailes/'+id;
    });
});

$(document).ready(() => {
    $('.crud-editar').click(function(){
        var id = $(this).val();

        window.location.href = 'http://127.0.0.1:5000/vehicles/edit/'+id;
    });
});

$(document).ready(() =>{
    $('.crud-eliminar').click(function(){
        var id = $(this).val();
        $.ajax({
            type:"GET",
            url:window.location.href+"/delete-vehicle",
            data: {
                id : id,
            },
            success:() =>{
                location.reload();
            }
        });
    })
});