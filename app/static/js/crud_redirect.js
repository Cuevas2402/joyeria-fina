
$(document).ready(() => {
    $('.crud-detalles').click(function(){
        var id = $(this).val();

        window.location.href = window.location.href+'/detailes/'+id;
    });
});

$(document).ready(() => {
    $('.crud-editar').click(function(){
        var id = $(this).val();

        window.location.href = window.location.href+'/edit/'+id;
    });
});

$(document).ready(() =>{
    $('.crud-eliminar').click(function(){
        var id = $(this).val();
        var type = $(this).attr('data-type');
        console.log(type);
        $.ajax({
            type:"GET",
            url:window.location.href+"/delete-"+type,
            data: {
                id : id,
            },
            success:() =>{
                location.reload();
            }
        });
    })
});