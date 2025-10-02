# app/models/gestor.py

import json
import os
from app.models.tarefa import Tarefa

class GestorDeTarefas:
    def __init__(self, caminho_arquivo="tarefas.json"):
        self.caminho_arquivo = caminho_arquivo
        self.tarefas = []
        self.carregar_tarefas()

    def adicionar_tarefa(self, tarefa: Tarefa):
        self.tarefas.append(tarefa)
        self.salvar_tarefas()

    def remover_tarefa(self, id_tarefa):
        self.tarefas = [t for t in self.tarefas if t.id != id_tarefa]
        self.salvar_tarefas()

    def listar_tarefas(self):
        return self.tarefas

    def buscar_por_id(self, id_tarefa):
        for t in self.tarefas:
            if t.id == id_tarefa:
                return t
        return None

    def salvar_tarefas(self):
        with open(self.caminho_arquivo, "w") as f:
            json.dump([t.to_dict() for t in self.tarefas], f, indent=4)
    
    def partilhar_tarefas(self, caminho_destino):
        with open(caminho_destino, "w") as f:
            json.dump([t.to_dict() for t in self.tarefas], f, indent=4)

    def carregar_tarefas(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r") as f:
                dados = json.load(f)
                self.tarefas = [Tarefa.from_dict(t) for t in dados]
