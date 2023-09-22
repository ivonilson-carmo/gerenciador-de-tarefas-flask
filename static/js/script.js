$(document).on('change', 'input[name="check-task"]', event=>{
    event.preventDefault();
    const identify = event.target.value;

    $.ajax({
        url: '/',
        type: 'post',
        data: { action: 'check', identify },
        success: function (response){
            const msg = `Completada em: ${response.data}`
            event.target.parentNode.querySelector('p.date-finished').innerText = msg;
            event.target.disabled = true;
        }
    }); //  fim da requisição
}); // fim da função

$(document).on('submit', 'form.remove',  event => {
    event.preventDefault();
    const identify = event.target.querySelector('input').value
    const itemTask = event.target.parentNode
    
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
        const task = document.querySelector('.content-header input.text-task');
        event.preventDefault()
        
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
                        <div class="item-task">
                        <input type="checkbox" name="check-task" value="${response.identify}" " >
                        <div>
                            <h2 class="title" id="${response.identify}"> ${response.task} </h2>
                            <p class="date-created"> Criado em: ${response.date_created} </p>
                            <p class="date-finished">  </p>
                        </div>
                        <form action="/remove" method="post" class="remove">
                            <input type="text" value="${response.identify}" name="identify">
                            <button>
                                <i class="bi bi-x-square"></i>
                            </button>
                        </form>
                    </div>`
                    document.querySelector('.content-task').innerHTML += template
                    task.value = '';
                }
            }); // fim do ajax
        } // fim do else
}) // fim da escuta do evento
