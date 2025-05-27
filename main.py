# main.py

from app.models.gestor import GestorDeTarefas
from app.models.tarefa import Tarefa
from app.models.relatorio import Relatorio


def gerar_relatorio(gestor):
    rel = Relatorio(gestor.listar_tarefas())

    print("\n📊 RELATÓRIO DE TAREFAS:")

    status = rel.contar_por_status()
    print(f"Pendentes: {status['pendentes']}")
    print(f"Concluídas: {status['concluidas']}")

    print("\n⏰ Tarefas vencidas:")
    for t in rel.tarefas_vencidas():
        print(f"- {t.titulo} (vencia em {t.data_limite})")

    print("\n🚦 Prioridades:")
    for p, qtd in rel.por_prioridade().items():
        print(f"{p.capitalize()}: {qtd}")

    print("\n📂 Categorias:")
    for c, qtd in rel.por_categoria().items():
        print(f"{c.capitalize()}: {qtd}")


def mostrar_menu():
    print("\n📋 TAREFA PRO+")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Concluir tarefa")
    print("4. Remover tarefa")
    print("5. Sair")
    print("6. Gerar relatório")

def adicionar_tarefa(gestor):
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    prioridade = input("Prioridade (baixa, media, alta): ")
    categoria = input("Categoria (ex: estudo, pessoal): ")
    data_limite = input("Data limite (YYYY-MM-DD): ")
    
    nova = Tarefa(titulo, descricao, prioridade, categoria, data_limite)
    gestor.adicionar_tarefa(nova)
    print("✅ Tarefa adicionada com sucesso!")

def listar_tarefas(gestor):
    tarefas = gestor.listar_tarefas()
    if not tarefas:
        print("⚠️ Nenhuma tarefa encontrada.")
        return

    for t in tarefas:
        print(f"\n🆔 ID: {t.id}")
        print(f"📌 Título: {t.titulo}")
        print(f"📖 Descrição: {t.descricao}")
        print(f"⏰ Prazo: {t.data_limite}")
        print(f"📂 Categoria: {t.categoria}")
        print(f"🚦 Prioridade: {t.prioridade}")
        print(f"📅 Criada em: {t.data_criacao}")
        print(f"✅ Status: {t.status}")

def concluir_tarefa(gestor):
    id_tarefa = input("ID da tarefa a concluir: ")
    tarefa = gestor.buscar_por_id(id_tarefa)
    if tarefa:
        tarefa.concluir()
        gestor.salvar_tarefas()
        print("✅ Tarefa concluída com sucesso!")
    else:
        print("❌ Tarefa não encontrada.")

def remover_tarefa(gestor):
    id_tarefa = input("ID da tarefa a remover: ")
    gestor.remover_tarefa(id_tarefa)
    print("🗑️ Tarefa removida (se existia).")

def main():
    gestor = GestorDeTarefas()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_tarefa(gestor)
        elif opcao == "2":
            listar_tarefas(gestor)
        elif opcao == "3":
            concluir_tarefa(gestor)
        elif opcao == "4":
            remover_tarefa(gestor)
        elif opcao == "5":
            print("👋 Saindo do programa...")
            break
        elif opcao == "6":
             gerar_relatorio(gestor)
             
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
