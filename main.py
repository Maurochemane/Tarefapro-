# main.py

from app.models.gestor import GestorDeTarefas
from app.models.tarefa import Tarefa
from app.models.relatorio import Relatorio
from datetime import datetime


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
    print("\n📋 TAREFA PRO++")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Concluir tarefa")
    print("4. Remover tarefa")
    print("5. Gerar relatório completo")
    print("6. Gerenciar tags")
    print("7. Gerenciar subtarefas")
    print("8. Configurar lembretes")
    print("9. Buscar tarefas")
    print("10. Fazer backup")
    print("11. Importar tarefas")
    print("12. Limpar concluídas")
    print("0. Sair")


def adicionar_tarefa(gestor):
    print("\n📝 NOVA TAREFA")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    prioridade = input("Prioridade (baixa, media, alta): ")
    categoria = input("Categoria: ")

    # Garante formato correto da data
    while True:
        try:
            data_str = input("Data limite (DD/MM/YYYY): ")
            data_limite = datetime.strptime(
                data_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            break
        except ValueError:
            print("❌ Formato de data inválido. Use DD/MM/YYYY")

    nova = Tarefa(titulo, descricao, prioridade, categoria, data_limite)

    # Adicionar tags
    if input("Deseja adicionar tags? (s/n): ").lower() == 's':
        tags = input("Tags (separadas por vírgula): ").split(',')
        for tag in tags:
            nova.adicionar_tag(tag.strip())

    # Tempo estimado
    if input("Deseja adicionar tempo estimado? (s/n): ").lower() == 's':
        horas = float(input("Horas estimadas: "))
        nova.definir_tempo_estimado(horas)

    # Recorrência
    if input("Deseja tornar a tarefa recorrente? (s/n): ").lower() == 's':
        tipo = input("Tipo (diaria/semanal/mensal): ")
        intervalo = int(input("Intervalo: "))
        nova.definir_recorrencia(tipo, intervalo)

    gestor.adicionar_tarefa(nova)
    print("✅ Tarefa adicionada com sucesso!")


def listar_tarefas(gestor, tarefas=None):
    if tarefas is None:
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


def gerenciar_tags(gestor):
    print("\n🏷️ GERENCIAR TAGS")
    id_tarefa = input("ID da tarefa: ")
    tarefa = gestor.buscar_por_id(id_tarefa)
    if tarefa:
        print(f"Tags atuais: {', '.join(tarefa.tags)}")
        opcao = input("1. Adicionar tag\n2. Remover tag\nEscolha: ")
        if opcao == "1":
            tag = input("Nova tag: ")
            tarefa.adicionar_tag(tag)
        elif opcao == "2":
            tag = input("Tag a remover: ")
            tarefa.remover_tag(tag)
        gestor.salvar_tarefas()
    else:
        print("❌ Tarefa não encontrada.")


def gerenciar_subtarefas(gestor):
    print("\n📑 GERENCIAR SUBTAREFAS")
    id_tarefa = input("ID da tarefa: ")
    tarefa = gestor.buscar_por_id(id_tarefa)
    if tarefa:
        while True:
            print("\n1. Adicionar subtarefa")
            print("2. Concluir subtarefa")
            print("3. Listar subtarefas")
            print("4. Voltar")

            opcao = input("Escolha: ")
            if opcao == "1":
                desc = input("Descrição da subtarefa: ")
                tarefa.adicionar_subtarefa(desc)
            elif opcao == "2":
                id_sub = input("ID da subtarefa: ")
                tarefa.concluir_subtarefa(id_sub)
            elif opcao == "3":
                for sub in tarefa.subtarefas:
                    status = "✅" if sub["concluida"] else "⭕"
                    print(f"{status} {sub['id']}: {sub['descricao']}")
            elif opcao == "4":
                break
        gestor.salvar_tarefas()
    else:
        print("❌ Tarefa não encontrada.")


def buscar_tarefas(gestor):
    print("\n🔍 BUSCAR TAREFAS")
    print("1. Por tag")
    print("2. Por categoria")
    print("3. Por prioridade")
    print("4. Tarefas atrasadas")
    print("5. Tarefas para hoje")

    opcao = input("Escolha: ")
    if opcao == "1":
        tag = input("Tag: ")
        tarefas = gestor.buscar_por_tag(tag)
    elif opcao == "2":
        categoria = input("Categoria: ")
        tarefas = gestor.buscar_por_categoria(categoria)
    elif opcao == "3":
        prioridade = input("Prioridade: ")
        tarefas = gestor.buscar_por_prioridade(prioridade)
    elif opcao == "4":
        tarefas = gestor.buscar_tarefas_atrasadas()
    elif opcao == "5":
        tarefas = gestor.buscar_tarefas_para_hoje()
    else:
        print("Opção inválida")
        return

    listar_tarefas(gestor, tarefas)


def gerar_relatorio_completo(gestor):
    rel = Relatorio(gestor.listar_tarefas())
    resultado = rel.resumo_completo()

    print("\n📊 RELATÓRIO COMPLETO")
    print(f"\n📈 Status:")
    print(f"Pendentes: {resultado['status']['pendentes']}")
    print(f"Concluídas: {resultado['status']['concluidas']}")

    print(f"\n⏰ Tarefas vencidas: {resultado['vencidas']}")

    print("\n⚡ Análise de tempo:")
    print(
        f"Tempo total estimado: {resultado['tempo']['tempo_total_estimado']}h")
    print(f"Tempo total gasto: {resultado['tempo']['tempo_total_gasto']}h")

    print("\n📑 Subtarefas:")
    print(f"Total: {resultado['subtarefas']['total_subtarefas']}")
    print(f"Concluídas: {resultado['subtarefas']['subtarefas_concluidas']}")

    print("\n🏷️ Tags mais usadas:")
    for tag, count in resultado['tags']['tags_mais_usadas'].items():
        print(f"{tag}: {count}")


def configurar_lembretes(gestor):
    print("\n⏰ CONFIGURAR LEMBRETES")
    id_tarefa = input("ID da tarefa: ")
    tarefa = gestor.buscar_por_id(id_tarefa)

    if tarefa:
        print("\nLembretes atuais:")
        for lembrete in tarefa.listar_lembretes():
            print(f"- {lembrete}")

        print("\n1. Adicionar novo lembrete")
        print("2. Voltar")

        opcao = input("\nEscolha uma opção: ")
        if opcao == "1":
            data_lembrete = input("Data do lembrete (DD/MM/YYYY): ")
            hora_lembrete = input("Hora do lembrete (HH:MM): ")

            if tarefa.adicionar_lembrete(data_lembrete, hora_lembrete):
                gestor.salvar_tarefas()
                print("✅ Lembrete configurado com sucesso!")
            else:
                print("❌ Erro ao configurar lembrete")
    else:
        print("❌ Tarefa não encontrada.")


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
            gerar_relatorio_completo(gestor)
        elif opcao == "6":
            gerenciar_tags(gestor)
        elif opcao == "7":
            gerenciar_subtarefas(gestor)
        elif opcao == "8":
            configurar_lembretes(gestor)
        elif opcao == "9":
            buscar_tarefas(gestor)
        elif opcao == "10":
            caminho = input("Caminho para backup: ")
            if gestor.fazer_backup(caminho):
                print("✅ Backup realizado com sucesso!")
            else:
                print("❌ Erro ao fazer backup")
        elif opcao == "11":
            caminho = input("Caminho do arquivo para importar: ")
            if gestor.importar_tarefas(caminho):
                print("✅ Tarefas importadas com sucesso!")
            else:
                print("❌ Erro ao importar tarefas")
        elif opcao == "12":
            qtd = gestor.limpar_tarefas_concluidas()
            print(f"✨ {qtd} tarefas concluídas foram removidas")
        elif opcao == "0":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")


if __name__ == "__main__":
    main()
