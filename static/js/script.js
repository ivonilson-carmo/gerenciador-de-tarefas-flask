$(document).on('change', 'input[name="check"]', event=>{
    event.preventDefault();
    const identify = event.target.value;

    $.ajax({
        url: '/',
        type: 'post',
        data: { action: 'check', identify },
        success: function (response){
            const msg = `Completada em: ${response.date}`
            event.target.parentNode.parentNode.querySelector('p.date-completed').innerText = msg;
            event.target.disabled = true;
        }
    }); //  fim da requisição
}); // fim da função


$(document).on('click', '.content-remove',  event => {
    event.preventDefault();
    const identify = event.target.getAttribute('data-id')
    const itemTask = event.target.parentNode.parentNode // div.item-task
    
    $.ajax({
        url: '/',
        type: 'post',
        data: { identify , action: 'remove'},
        success: function(response){
            itemTask.parentNode.removeChild(itemTask);
        },
    }); // fim da requisição
}); // fim da função


$(document).on('submit', '.content-header form', event => {
        // só chama o a função para acrescentar tarefa se tiver texto digitado das tarefas
        const task = document.querySelector('.content-header input');
        event.preventDefault()
        console.log('oi')
        if (task.value == ''){
            alert('Digite algo para continuar!!');
        }else{
            // requisição para acrescentar tarefa
            $.ajax({
                url: "/",
                type: "post",
                data: {task: task.value, action: 'add'},
                success: function(response) {
                    let template = `
                        <div class="iten-task mb-3 d-flex mx-2 p-2 border-1 border-bottom">
                            <form action="" class="check-task" class="d-flex">
                                <input type="checkbox" name="check" id="check-task" value="${response.identify} ">
                            </form>

                            <div class="content-info m-0 row flex-grow-1">
                                <p class="title-task fs-6 col-12 text-break mb-1"> ${task.value} </p>
                                <p class="date-created col-sm-12 col-md-6 mb-0"> Criado em: ${response.date_created} </p>
                                <p class="date-completed col-sm-12 col-md-6 mb-0"> </p>
                            </div> <!-- fim content-info -->
                            <div class="content-remove d-flex">
                                <i class="bi bi-x-lg py-3 px-3 align-self-center" data-id="${response.identify}" ></i>
                            </div>
                            </div> <!-- Fim item-task --> `
                    document.querySelector('.content-task').innerHTML += template
                    task.value = '';
                }
            }); // fim do ajax
        } // fim do else
}) // fim da escuta do evento
