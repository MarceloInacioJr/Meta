const btnMensagem = document.querySelector('#fechar-menssagem');

btnMensagem.addEventListener('click', () =>{
    let menssagem = document.querySelector('.form-menssagem');

    menssagem.classList.add('fechar')
})