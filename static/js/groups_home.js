window.onload=function(){
    var button = document.getElementById('button')

    if (button) {
    button.addEventListener('click',
        function() {
            document.querySelector('.modal-background').style.display = 'flex';
    });

    document.querySelector('.close').addEventListener('click', 
    function() {
        document.querySelector('.modal-background').style.display = 'none';
    })
    }
}