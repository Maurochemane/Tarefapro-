# app/models/tarefa.py

import uuid
from datetime import datetime

class Tarefa:
    def __init__(self, titulo, descricao, prioridade, categoria, data_limite):
        self.id = str(uuid.uuid1()) # ID único automático
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade  # baixa, média, alta
        self.categoria = categoria    # exemplo: estudo, trabalho, pessoal
        self.data_criacao = datetime.now().isoformat()
        self.data_limite = data_limite
        self.status = "pendente"      # ou "concluída"

    def concluir(self):
        self.status = "concluída"

    def to_dict(self):
        """Retorna a tarefa como dicionário (útil para salvar em JSON)"""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "prioridade": self.prioridade,
            "categoria": self.categoria,
            "data_criacao": self.data_criacao,
            "data_limite": self.data_limite,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Cria uma Tarefa a partir de um dicionário (útil para carregar do JSON)"""
        tarefa = cls(
            titulo=data["titulo"],
            descricao=data["descricao"],
            prioridade=data["prioridade"],
            categoria=data["categoria"],
            data_limite=data["data_limite"]
        )
        tarefa.id = data["id"]
        tarefa.data_criacao = data["data_criacao"]
        tarefa.status = data["status"]
        return tarefa
