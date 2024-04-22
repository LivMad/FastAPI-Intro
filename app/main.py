from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException, status


class ItemTodo(BaseModel):  # Usuário não acessa porque não indica o id.
    id: int
    titulo: str
    descricao: str
    concluido: bool = False


class ItemTodoUsuario(BaseModel):  # Acesso do usuário.
    titulo: str
    descricao: str
    concluido: bool = False


class ItemTodoEditar(
    BaseModel
):  # Acesso do usuário. É opcional as edições, por isso o None = None.
    titulo: str | None = None
    descricao: str | None = None
    concluido: bool | None = None


app = FastAPI()

lista = []


@app.post("/tarefas/")
async def lista_tarefas(
    tarefa: ItemTodoUsuario,
):  # Criação de uma nova classe, porque o usuário não escolhe o id.
    id = len(lista)  # id é o índice da lista.
    lista.append(tarefa)
    return ItemTodo(
        id=id, **tarefa.model_dump()
    )  # model_dump() é apenas para objetos do pydantic.


@app.get("/tarefas/{tarefa_id}")
async def tarefa_path(tarefa_id: int):
    if tarefa_id >= len(lista) or lista[tarefa_id] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com id={tarefa_id} não encontrado!",
        )

    if (
        tarefa_id < len(lista) and lista[tarefa_id] is not None
    ):  # Só roda com id existente.
        return ItemTodo(id=tarefa_id, **lista[tarefa_id].model_dump())


@app.get(
    "/tarefas/"
)  # mesmo path para um mesmo método deve abranger funções e comandos relacionados à ele.
async def tarefas_completas(
    completo: bool | None = None,
):  # Depois do = só pode ter uma coisa.
    lista_tarefa_completa = []
    lista_tarefa_incompleta = []
    lista_tarefa_todas = []
    for i in range(len(lista)):
        if lista[i] is not None:
            if lista[i].concluido is True:
                lista_tarefa_completa.append(ItemTodo(id=i, **lista[i].model_dump()))
            if lista[i].concluido is False:
                lista_tarefa_incompleta.append(ItemTodo(id=i, **lista[i].model_dump()))
            lista_tarefa_todas.append(ItemTodo(id=i, **lista[i].model_dump()))

    if completo is True:  # comandos relacionados ao mesmo path.
        return lista_tarefa_completa
    if completo is False:
        return lista_tarefa_incompleta
    if completo is None:
        return lista_tarefa_todas


@app.patch("/tarefas/{tarefa_id}")
async def editar_tarefas(tarefa_id: int, tarefa_editada: ItemTodoEditar):
    if tarefa_id >= len(lista) or lista[tarefa_id] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com id={tarefa_id} não encontrado!",
        )
    if tarefa_id < len(lista):
        item_antigo = lista[
            tarefa_id
        ]  # É preciso inserir outro objeto do mesmo tipo pré-existente, a ideia é acessar o objeto,
        # editar os campos que vieram do body e inserir o objeto modificado.

        if tarefa_editada.titulo is not None:
            item_antigo.titulo = tarefa_editada.titulo

        if tarefa_editada.descricao is not None:
            item_antigo.descricao = tarefa_editada.descricao

        if tarefa_editada.concluido is not None:
            item_antigo.concluido = tarefa_editada.concluido

    lista.insert(
        tarefa_id, item_antigo
    )  # Após atualização de cada atributo do objeto, faz-se a adição do objeto editado.
    del lista[tarefa_id + 1]  # Apaga-se o objeto velho.
    return ItemTodo(id=tarefa_id, **lista[tarefa_id].model_dump())


@app.delete("/tarefas/{tarefa_id}")
async def deletar_tarefa(tarefa_id: int):
    if tarefa_id >= len(lista) or lista[tarefa_id] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com id={tarefa_id} não encontrado!",
        )
    else:  # O id não é excluído, apenas os atributos relacionados à ele.
        lista.insert(tarefa_id, None)
        del lista[tarefa_id + 1]
