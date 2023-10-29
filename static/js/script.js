$(document).on('change', 'input[name="check"]', event=>{
    const identify = event.target.value;
    event.preventDefault();
    
    $.ajax({
        url: '/task/update',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            id: identify
        }),
        success: function (response){
            if (response.error){
                alert(`Erro durante sua solicitação: ${response.error}`)
            }else{
                const msg = `Completada em: ${response.date_completed}`
                event.target.parentNode.parentNode.querySelector('p.date-completed').innerText = msg;
                event.target.disabled = true;
            }
        }
    }); 
}); 


$(document).on('click', '.content-remove',  event => {
    event.preventDefault();
    const identify = event.target.getAttribute('data-id')
    const itemTask = event.target.parentNode.parentNode 
    
    $.ajax({
        url: '/task/remove',
        type: 'POST',
        data: JSON.stringify({ id:  identify }),
        contentType: 'application/json',
        success: function(response){
            if (response.error){
                alert(`Erro durante solicitação: ${response.error}`);
            }else{
                itemTask.parentNode.removeChild(itemTask);
            }
        },
    }); 
}); 


$(document).on('submit', '.content-header form', event => {
        const task = document.querySelector('.content-header input');
        event.preventDefault()
        
        if (task.value == ''){
            alert('Digite algo para continuar!!');
        }else{
            $.ajax({
                url: "/task/add",
                type: "POST",
                data: JSON.stringify({task: task.value}),
                contentType: 'application/json',
                success: function(response) {
                    if(response.error){
                        alert(`Erro durante solicitação: ${response.error}`);
                    }else{
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
                    }
            }); 
        } 
}) 
