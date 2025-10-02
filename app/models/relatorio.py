# app/models/relatorio.py

from datetime import datetime
from collections import defaultdict


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
                    raise ValueError(
                        f"Erro na data da tarefa '{t.titulo}': {str(e)}")

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

    def analise_tempo(self):
        """Análise de tempo estimado vs tempo gasto"""
        total_estimado = sum(t.tempo_estimado or 0 for t in self.tarefas)
        total_gasto = sum(t.tempo_gasto or 0 for t in self.tarefas)
        tarefas_atrasadas = [t for t in self.tarefas
                             if t.tempo_gasto and t.tempo_estimado
                             and t.tempo_gasto > t.tempo_estimado]

        return {
            "tempo_total_estimado": total_estimado,
            "tempo_total_gasto": total_gasto,
            "tarefas_que_excederam_estimativa": len(tarefas_atrasadas)
        }

    def analise_subtarefas(self):
        """Análise das subtarefas"""
        total_subtarefas = sum(len(t.subtarefas) for t in self.tarefas)
        subtarefas_concluidas = sum(
            sum(1 for s in t.subtarefas if s["concluida"])
            for t in self.tarefas
        )

        return {
            "total_subtarefas": total_subtarefas,
            "subtarefas_concluidas": subtarefas_concluidas,
            "subtarefas_pendentes": total_subtarefas - subtarefas_concluidas
        }

    def analise_tags(self):
        """Análise das tags mais usadas"""
        tag_counter = defaultdict(int)
        for tarefa in self.tarefas:
            for tag in tarefa.tags:
                tag_counter[tag] += 1

        # Ordenar tags por frequência
        tags_ordenadas = sorted(
            tag_counter.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "total_tags_unicas": len(tag_counter),
            "tags_mais_usadas": dict(tags_ordenadas[:5])
        }

    def tarefas_recorrentes(self):
        """Análise de tarefas recorrentes"""
        recorrentes = [t for t in self.tarefas if t.recorrencia]
        tipos_recorrencia = defaultdict(int)

        for tarefa in recorrentes:
            tipos_recorrencia[tarefa.recorrencia["tipo"]] += 1

        return {
            "total_recorrentes": len(recorrentes),
            "distribuicao": dict(tipos_recorrencia)
        }

    def resumo_completo(self):
        """Gera um resumo completo com todas as análises"""
        return {
            "status": self.contar_por_status(),
            "prioridades": self.por_prioridade(),
            "categorias": self.por_categoria(),
            "vencidas": len(self.tarefas_vencidas()),
            "tempo": self.analise_tempo(),
            "subtarefas": self.analise_subtarefas(),
            "tags": self.analise_tags(),
            "recorrencia": self.tarefas_recorrentes()
        }

    def tarefas_por_tag(self, tag):
        """Retorna todas as tarefas com uma determinada tag"""
        return [t for t in self.tarefas if tag in t.tags]

    def progresso_por_categoria(self):
        """Calcula o progresso percentual por categoria"""
        categorias = defaultdict(lambda: {"total": 0, "concluidas": 0})

        for tarefa in self.tarefas:
            categorias[tarefa.categoria]["total"] += 1
            if tarefa.status == "concluída":
                categorias[tarefa.categoria]["concluidas"] += 1

        resultado = {}
        for categoria, dados in categorias.items():
            resultado[categoria] = {
                "total": dados["total"],
                "concluidas": dados["concluidas"],
                "percentual": (dados["concluidas"] / dados["total"]) * 100
            }

        return resultado
