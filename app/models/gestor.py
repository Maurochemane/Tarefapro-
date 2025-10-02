# app/models/gestor.py

import json
import os
from datetime import datetime
from app.models.tarefa import Tarefa
from typing import List, Optional


class GestorDeTarefas:
    def __init__(self, caminho_arquivo="tarefas.json"):
        self.caminho_arquivo = caminho_arquivo
        self.tarefas = []
        self.carregar_tarefas()

    def adicionar_tarefa(self, tarefa: Tarefa) -> None:
        self.tarefas.append(tarefa)
        self.salvar_tarefas()

    def remover_tarefa(self, id_tarefa: str) -> bool:
        tamanho_inicial = len(self.tarefas)
        self.tarefas = [t for t in self.tarefas if t.id != id_tarefa]
        self.salvar_tarefas()
        return len(self.tarefas) < tamanho_inicial

    def listar_tarefas(self):
        return self.tarefas

    def buscar_por_id(self, id_tarefa):
        for t in self.tarefas:
            if t.id == id_tarefa:
                return t
        return None

    def buscar_por_tag(self, tag: str) -> List[Tarefa]:
        return [t for t in self.tarefas if tag in t.tags]

    def buscar_por_categoria(self, categoria: str) -> List[Tarefa]:
        return [t for t in self.tarefas if t.categoria.lower() == categoria.lower()]

    def buscar_por_prioridade(self, prioridade: str) -> List[Tarefa]:
        return [t for t in self.tarefas if t.prioridade.lower() == prioridade.lower()]

    def _converter_data(self, data_str):
        """Converte diferentes formatos de data para objeto datetime."""
        formatos = [
            "%d-%m-%Y",  # 03-10-2025
            "%d/%m/%Y",  # 03/10/2025
            "%Y-%m-%d",  # 2025-10-03
            "%d.%m.%Y",  # 03.10.2025
        ]

        if isinstance(data_str, datetime):
            return data_str.date()

        for formato in formatos:
            try:
                return datetime.strptime(data_str, formato).date()
            except ValueError:
                continue

        raise ValueError(f"Formato de data inválido: {data_str}")

    def buscar_tarefas_atrasadas(self) -> List[Tarefa]:
        hoje = datetime.now().date()
        return [t for t in self.tarefas
                if t.status == "pendente"
                and self._converter_data(t.data_limite) < hoje]

    def buscar_tarefas_para_hoje(self) -> List[Tarefa]:
        hoje = datetime.now().date()
        return [t for t in self.tarefas if t.status == "pendente"
                and self._converter_data(t.data_limite) == hoje]
        # and datetime.fromisoformat(t.data_limite).date() == hoje]

    def atualizar_tarefa(self, id_tarefa: str, dados: dict) -> bool:
        tarefa = self.buscar_por_id(id_tarefa)
        if tarefa:
            for chave, valor in dados.items():
                if hasattr(tarefa, chave):
                    setattr(tarefa, chave, valor)
            self.salvar_tarefas()
            return True
        return False

    def concluir_tarefa(self, id_tarefa: str) -> bool:
        tarefa = self.buscar_por_id(id_tarefa)
        if tarefa:
            tarefa.concluir()
            if tarefa.recorrencia:
                proxima_tarefa = tarefa.gerar_proxima_tarefa()
                self.adicionar_tarefa(proxima_tarefa)
            self.salvar_tarefas()
            return True
        return False

    def salvar_tarefas(self):
        """Salva as tarefas em JSON"""
        dados = [t.to_dict() for t in self.tarefas]
        with open(self.caminho_arquivo, "w") as f:
            json.dump(dados, f, indent=2)

    def partilhar_tarefas(self, caminho_destino):
        with open(caminho_destino, "w") as f:
            json.dump([t.to_dict() for t in self.tarefas], f, indent=4)

    def carregar_tarefas(self):
        """Carrega as tarefas do arquivo JSON"""
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r") as f:
                dados = json.load(f)
                self.tarefas = [Tarefa.from_dict(t) for t in dados]

    def fazer_backup(self, caminho_backup: str) -> bool:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"backup_tarefas_{timestamp}.json"
            caminho_completo = os.path.join(caminho_backup, nome_arquivo)
            self.partilhar_tarefas(caminho_completo)
            return True
        except Exception:
            return False

    def importar_tarefas(self, caminho_arquivo: str) -> bool:
        try:
            with open(caminho_arquivo, "r") as f:
                dados = json.load(f)
                novas_tarefas = [Tarefa.from_dict(t) for t in dados]
                self.tarefas.extend(novas_tarefas)
                self.salvar_tarefas()
                return True
        except Exception:
            return False

    def limpar_tarefas_concluidas(self) -> int:
        quantidade_inicial = len(self.tarefas)
        self.tarefas = [t for t in self.tarefas if t.status != "concluída"]
        self.salvar_tarefas()
        return quantidade_inicial - len(self.tarefas)

    def obter_estatisticas(self) -> dict:
        total = len(self.tarefas)
        concluidas = sum(1 for t in self.tarefas if t.status == "concluída")
        categorias = {}
        prioridades = {"baixa": 0, "media": 0, "alta": 0}

        for t in self.tarefas:
            categorias[t.categoria] = categorias.get(t.categoria, 0) + 1
            prioridades[t.prioridade] = prioridades.get(t.prioridade, 0) + 1

        return {
            "total_tarefas": total,
            "concluidas": concluidas,
            "pendentes": total - concluidas,
            "distribuicao_categorias": categorias,
            "distribuicao_prioridades": prioridades
        }
