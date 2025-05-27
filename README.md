#estructura do projecto
tarefa_pro/
│
├── app/                     # Código principal do aplicativo
│   ├── __init__.py          # Torna o diretório um pacote Python
│   ├── models/              # Classes principais (POO): Tarefa, Gestor, Relatorio
│   ├── storage/             # Módulos de persistência: JSON ou DB
│   ├── api/                 # API com Flask: rotas, controladores
│   └── utils/               # Funções auxiliares: datas, validações, formatações
│
├── main.py                  # Ponto de entrada para a aplicação (modo CLI)
├── requirements.txt         # Lista de bibliotecas necessárias
├── README.md                # Explicação do projeto (início da documentação)
└── tests/                   # Testes unitários

# 📝 TarefaPro+

**TarefaPro+** é um sistema simples e poderoso de gerenciamento de tarefas, desenvolvido em Python com Flask, que permite criar, listar, atualizar e deletar tarefas, além de gerar relatórios detalhados. O projeto é voltado ao aprendizado de arrays, dicionários, orientação a objetos, manipulação de arquivos e APIs RESTful.

---

## 🚀 Funcionalidades

- ✅ Adicionar novas tarefas
- 📋 Listar todas as tarefas
- ✏️ Marcar tarefas como concluídas
- ❌ Deletar tarefas
- 📊 Gerar relatório com:
  - Total de tarefas por status
  - Por prioridade
  - Por categoria
  - Tarefas vencidas

---

## 📁 Estrutura de Pastas
TarefaPro+/
├── app/
│ ├── init.py
│ ├── server.py # Servidor Flask
│ ├── api/
│ │ └── routes.py # Rotas da API
│ └── models/
│ ├── tarefa.py # Classe Tarefa
│ ├── gestor.py # Classe GestorTarefas
│ └── relatorio.py # Classe RelatorioTarefas
├── data/
│ └── tarefas.json # Armazenamento das tarefas



---

## 🧪 Como Usar

### 🔧 Requisitos

- Python 3.10+
- Flask

### 📦 Instalar dependências

```bash
pip install flask


Rodar o servidor
Vá até o diretório do projeto:

bash
Copiar
Editar
cd TarefaPro+
Rode com:

bash
Copiar
Editar
python -m app.server
O servidor estará disponível em http://127.0.0.1:5000.

🔌 Rotas da API
Método	Rota	Descrição
GET	/tarefas	Lista todas as tarefas
POST	/tarefas	Adiciona nova tarefa
PUT	/tarefas/<id>	Marca tarefa como concluída
DELETE	/tarefas/<id>	Remove uma tarefa
GET	/relatorio	Gera relatório de tarefas

📌 Exemplo de JSON para POST
json

{
  "titulo": "Estudar Flask",
  "descricao": "Criar API para tarefas",
  "prioridade": "alta",
  "categoria": "programacao",
  "data_limite": "2025-06-01"
}
💡 Aprendizados Técnicos
Orientação a Objetos (Classes, Métodos, Encapsulamento)

Manipulação de arquivos JSON

API com Flask (Blueprints e rotas RESTful)

Organização modular de projeto em Python

Boas práticas com __init__.py e server.py

📚 Autor
Mauro Venancio Chemane
Estudante e desenvolvedor apaixonado por aprender Python de forma prática e aplicável.
📍 Maputo, Mozambique

