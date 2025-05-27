# app/api/routes.py

from flask import Blueprint, jsonify, request
from app.models.gestor import GestorDeTarefas
from app.models.tarefa import Tarefa
from app.models.relatorio import Relatorio

rotas = Blueprint("rotas", __name__)
gestor = GestorDeTarefas()

@rotas.route("/tarefas", methods=["GET"])
def listar_tarefas():
    tarefas = [t.to_dict() for t in gestor.listar_tarefas()]
    return jsonify(tarefas)

@rotas.route("/tarefas", methods=["POST"])
def adicionar_tarefa():
    dados = request.json
    nova = Tarefa(
        dados["titulo"],
        dados.get("descricao", ""),
        dados.get("prioridade", "media"),
        dados.get("categoria", "geral"),
        dados["data_limite"]
    )
    gestor.adicionar_tarefa(nova)
    return jsonify({"mensagem": "Tarefa adicionada com sucesso!"}), 201

@rotas.route("/tarefas/<id>", methods=["PUT"])
def concluir_tarefa(id):
    tarefa = gestor.buscar_por_id(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    tarefa.concluir()
    gestor.salvar_tarefas()
    return jsonify({"mensagem": "Tarefa marcada como concluída."})

@rotas.route("/tarefas/<id>", methods=["DELETE"])
def remover_tarefa(id):
    gestor.remover_tarefa(id)
    return jsonify({"mensagem": "Tarefa removida (se existia)."}), 204

@rotas.route("/relatorio", methods=["GET"])
def relatorio():
    rel = Relatorio(gestor.listar_tarefas())
    dados = {
        "status": rel.contar_por_status(),
        "prioridade": rel.por_prioridade(),
        "categoria": rel.por_categoria(),
        "vencidas": [t.to_dict() for t in rel.tarefas_vencidas()]
    }
    return jsonify(dados)
