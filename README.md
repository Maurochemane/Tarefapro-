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
