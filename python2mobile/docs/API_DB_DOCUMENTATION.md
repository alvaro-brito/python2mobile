# Documentação: API e Banco de Dados Local no P2M

**Data:** 27 de Fevereiro de 2026
**Status:** ✅ Concluído

Este documento detalha a implementação e o uso das novas funcionalidades de **chamada de API** e **banco de dados local** no Python2Mobile (P2M).

---

## 🎯 Objetivo

O objetivo foi estender o P2M para suportar duas funcionalidades essenciais em aplicações modernas:

1.  **Comunicação com APIs Externas:** Permitir que as aplicações P2M façam requisições HTTP (GET, POST, etc.) para buscar ou enviar dados a servidores externos.
2.  **Persistência de Dados Locais:** Oferecer uma maneira de armazenar dados localmente no dispositivo do usuário, garantindo que as informações não se percam quando o aplicativo é fechado.

---

## ✅ Implementação

Foram criados dois novos módulos no core do P2M:

### 1. Módulo de API (`p2m/core/api.py`)

-   **`APIClient`:** Uma classe que abstrai a complexidade das requisições HTTP. Suporta os métodos `GET`, `POST`, `PUT` e `DELETE`.
-   **`init_api()` e `get_api()`:** Funções para inicializar e obter uma instância global do `APIClient`, facilitando o uso em toda a aplicação.
-   **Tradução para Nativos:**
    -   **Flutter:** O gerador de código utiliza o pacote `http` para fazer as requisições.
    -   **React Native:** Utiliza a `Fetch API` nativa do JavaScript.
    -   **Web:** Utiliza a `Fetch API` do navegador.

### 2. Módulo de Banco de Dados (`p2m/core/database.py`)

-   **`Database` (Abstrato):** Uma classe base que define a interface para operações de banco de dados (`set`, `get`, `delete`, etc.).
-   **`LocalDatabase`:** Uma implementação em memória para testes no DevServer.
-   **`Table`:** Uma classe que simula uma tabela de banco de dados, permitindo operações como `insert`, `get`, `update` e `delete` em um conjunto de dados específico.
-   **Tradução para Nativos:**
    -   **Flutter:** O gerador de código utiliza o pacote `shared_preferences` para armazenamento simples de chave-valor ou `sqflite` para bancos de dados mais complexos.
    -   **React Native:** Utiliza o `AsyncStorage` para persistência de dados.
    -   **Web:** Utiliza o `localStorage` do navegador.

---

## 🧪 Testes e Validação

-   **Novos Exemplos:** Foram criados dois novos exemplos de teste (`test_06_api_call.py` e `test_07_local_database.py`) para demonstrar o uso das novas funcionalidades.
-   **Testes E2E:** Os novos exemplos foram adicionados à suíte de testes E2E, e todos os 7 testes passaram com sucesso, validando a sintaxe e a estrutura dos novos exemplos.
-   **Validação da Geração de Código:** Foram criados testes específicos (`test_code_generation_examples.py`) para validar como o código P2M para API e banco de dados é traduzido para Flutter, React Native e Web. Todos os testes passaram, confirmando que a tradução está correta e utiliza as melhores práticas de cada plataforma.

---

## 🚀 Como Usar

### Chamada de API

```python
from p2m.core.api import init_api

# Inicializa a API com uma URL base
api = init_api(base_url="https://api.example.com")

async def fetch_users():
    # Faz uma requisição GET
    response = await api.get("/users")
    if response.success:
        print("Usuários encontrados:", response.data)
    else:
        print("Erro:", response.error)
```

### Banco de Dados Local

```python
from p2m.core.database import get_table

# Obtém uma "tabela" para armazenar usuários
users_table = get_table("users")

async def save_user(name, email):
    user_data = {"name": name, "email": email}
    # Insere um novo usuário
    await users_table.insert(email, user_data)

async def load_users():
    # Carrega todos os usuários
    all_users = await users_table.all()
    print("Todos os usuários:", all_users)
```

---

## Conclusão

As funcionalidades de chamada de API e banco de dados local foram implementadas, testadas e validadas com sucesso. O Python2Mobile agora é uma ferramenta ainda mais poderosa e completa para o desenvolvimento de aplicações multiplataforma, permitindo a criação de apps dinâmicos e conectados a dados.
