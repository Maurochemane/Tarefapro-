# app/models/relatorio.py

from datetime import datetime


class Relatorio:
    def __init__(self, tarefas):
        self.tarefas = tarefas

    def contar_por_status(self):
        pendentes = sum(1 for t in self.tarefas if t.status == "pendente")
        concluidas = sum(1 for t in self.tarefas if t.status == "concluída")
        return {"pendentes": pendentes, "concluidas": concluidas}

    def _converter_data(self, data_str):
        """Tenta converter diferentes formatos de data para ISO."""
        formatos = [
            "%d/%m/%Y",  # 31/12/2023
            "%d-%m-%Y",  # 31-12-2023
            "%Y-%m-%d",  # 2023-12-31
            "%d/%m/%y",  # 31/12/23
            "%d.%m.%Y",  # 31.12.2023
        ]
        
        if isinstance(data_str, datetime):
            return data_str.date()
            
        for formato in formatos:
            try:
                return datetime.strptime(data_str, formato).date()
            except ValueError:
                continue
                
        raise ValueError(
            "Formato de data inválido. Formatos aceitos: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD"
        )

    def tarefas_vencidas(self):
        hoje = datetime.now().date()
        vencidas = []
        
        for t in self.tarefas:
            if t.status == "pendente":
                try:
                    data_limite = self._converter_data(t.data_limite)
                    if data_limite < hoje:
                        vencidas.append(t)
                except ValueError as e:
                    raise ValueError(f"Erro na data da tarefa '{t.titulo}': {str(e)}")
                    
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
