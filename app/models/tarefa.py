# app/models/tarefa.py

import uuid
from datetime import datetime, timedelta


class Tarefa:
    def __init__(self, titulo, descricao, prioridade, categoria, data_limite):
        self.id = str(uuid.uuid1())  # ID único automático
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade  # baixa, média, alta
        self.categoria = categoria    # exemplo: estudo, trabalho, pessoal
        self.data_criacao = datetime.now().isoformat()
        self.data_limite = data_limite
        self.status = "pendente"      # ou "concluída"

        # Novas propriedades
        self.tags = []
        self.subtarefas = []
        self.lembretes = []
        self.recorrencia = None
        self.notas = ""
        self.tempo_estimado = None
        self.tempo_gasto = 0

    def adicionar_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remover_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def adicionar_subtarefa(self, descricao):
        subtarefa = {
            "id": str(uuid.uuid1()),
            "descricao": descricao,
            "concluida": False,
            "data_criacao": datetime.now().isoformat()
        }
        self.subtarefas.append(subtarefa)
        return subtarefa["id"]

    def concluir_subtarefa(self, subtarefa_id):
        for subtarefa in self.subtarefas:
            if subtarefa["id"] == subtarefa_id:
                subtarefa["concluida"] = True
                return True
        return False

    def adicionar_lembrete(self, data_str, hora_str):
        """Adiciona um lembrete combinando data e hora"""
        try:
            # Combina data e hora em um único datetime
            data = datetime.strptime(data_str, "%d/%m/%Y")
            hora = datetime.strptime(hora_str, "%H:%M").time()
            data_hora = datetime.combine(data.date(), hora)

            # Armazena no formato ISO
            self.lembretes.append(data_hora.isoformat())
            return True
        except ValueError as e:
            print(f"Erro ao configurar lembrete: {e}")
            return False

    def listar_lembretes(self):
        """Lista todos os lembretes formatados"""
        lembretes_formatados = []
        for lembrete in self.lembretes:
            data_hora = datetime.fromisoformat(lembrete)
            formatado = data_hora.strftime("%d/%m/%Y às %H:%M")
            lembretes_formatados.append(formatado)
        return lembretes_formatados

    def definir_recorrencia(self, tipo, intervalo=1):
        """
        tipo: 'diaria', 'semanal', 'mensal'
        intervalo: número de dias/semanas/meses entre recorrências
        """
        self.recorrencia = {
            "tipo": tipo,
            "intervalo": intervalo
        }

    def calcular_prioridade_dinamica(self):
        hoje = datetime.now()
        data_limite = datetime.fromisoformat(self.data_limite)
        dias_restantes = (data_limite - hoje).days

        if dias_restantes <= 1:
            return "URGENTE"
        elif dias_restantes <= 3:
            return "alta"
        elif dias_restantes <= 7:
            return "media"
        return "baixa"

    def adicionar_nota(self, nota):
        self.notas += f"\n[{datetime.now().isoformat()}] {nota}"

    def definir_tempo_estimado(self, horas):
        self.tempo_estimado = horas

    def registrar_tempo_gasto(self, horas):
        self.tempo_gasto += horas

    def gerar_proxima_tarefa(self):
        if not self.recorrencia:
            return None

        data_base = datetime.fromisoformat(self.data_limite)
        if self.recorrencia["tipo"] == "diaria":
            nova_data = data_base + \
                timedelta(days=self.recorrencia["intervalo"])
        elif self.recorrencia["tipo"] == "semanal":
            nova_data = data_base + \
                timedelta(weeks=self.recorrencia["intervalo"])
        elif self.recorrencia["tipo"] == "mensal":
            nova_data = data_base + \
                timedelta(days=30 * self.recorrencia["intervalo"])

        nova_tarefa = Tarefa(
            self.titulo,
            self.descricao,
            self.prioridade,
            self.categoria,
            nova_data.isoformat()
        )
        nova_tarefa.tags = self.tags.copy()
        nova_tarefa.tempo_estimado = self.tempo_estimado
        return nova_tarefa

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
            "status": self.status,
            "tags": self.tags,
            "subtarefas": self.subtarefas,
            "lembretes": self.lembretes,
            "recorrencia": self.recorrencia,
            "notas": self.notas,
            "tempo_estimado": self.tempo_estimado,
            "tempo_gasto": self.tempo_gasto
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
        tarefa.tags = data.get("tags", [])
        tarefa.subtarefas = data.get("subtarefas", [])
        tarefa.lembretes = data.get("lembretes", [])
        tarefa.recorrencia = data.get("recorrencia")
        tarefa.notas = data.get("notas", "")
        tarefa.tempo_estimado = data.get("tempo_estimado")
        tarefa.tempo_gasto = data.get("tempo_gasto", 0)
        return tarefa
