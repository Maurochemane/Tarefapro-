# app/models/relatorio.py

from datetime import datetime

class Relatorio:
    def __init__(self, tarefas):
        self.tarefas = tarefas

    def contar_por_status(self):
        pendentes = sum(1 for t in self.tarefas if t.status == "pendente")
        concluidas = sum(1 for t in self.tarefas if t.status == "concluída")
        return {"pendentes": pendentes, "concluidas": concluidas}

    def tarefas_vencidas(self):
        hoje = datetime.now().date()
        vencidas = [t for t in self.tarefas if t.status == "pendente" and datetime.fromisoformat(t.data_limite).date() < hoje]
        return vencidas

    def por_prioridade(self):
        prioridades = {"baixa": 0, "media": 0, "alta": 0}
        for t in self.tarefas:
            prioridades[t.prioridade] = prioridades.get(t.prioridade, 0) + 1
        return prioridades

    def por_categoria(self):
        categorias = {}
        for t in self.tarefas:
            categorias[t.categoria] = categorias.get(t.categoria, 0) + 1
        return categorias
