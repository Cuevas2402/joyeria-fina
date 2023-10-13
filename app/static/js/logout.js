$(document).ready(() => {
    $('#btn-logout').click(() =>{
        $.ajax({
            type: 'GET',
            url: '/logout', 
            success : () =>{
                location.reload();
            }
        });
    });
});