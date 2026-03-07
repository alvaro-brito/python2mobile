# Guia de Validação do P2M

**Data:** 27 de Fevereiro de 2026
**Status:** ✅ Concluído

Este documento detalha o sistema de validação de código do Python2Mobile (P2M).

---

## 🎯 O que é Validação?

A validação é um processo automático que verifica se o código P2M está correto e segue as melhores práticas antes de ser executado ou compilado. Isso ajuda a identificar e corrigir erros rapidamente.

---

## ✅ Validações Implementadas

O P2M valida automaticamente os seguintes aspectos do código:

### 1. Sintaxe Python
-   Verifica se o código Python é sintaticamente correto
-   Relata erros de sintaxe com linha e coluna exatas

### 2. Imports Obrigatórios
-   Verifica se `from p2m.core import Render` está presente
-   Verifica se `from p2m.ui import` está presente
-   Fornece avisos se imports estão faltando

### 3. Funções Obrigatórias
-   Verifica se a função `create_view()` existe
-   Verifica se a função `main()` existe
-   Relata erro se alguma função está faltando

### 4. Padrões Recomendados
-   Verifica se `create_view()` retorna `component.build()`
-   Verifica se `main()` chama `Render.execute(create_view)`
-   Fornece avisos se os padrões não são seguidos

---

## 🚀 Como Usar

### Validação Automática (Padrão)

Os comandos `p2m run` e `p2m build` executam validação automaticamente:

```bash
# Valida e executa o app
p2m run

# Valida e compila para Android
p2m build --target android
```

Se houver erros, o comando será interrompido:

```
🔍 Validating code...

❌ Validation failed:
   main.py:0:0 [ERROR] Missing required function: create_view()

💡 Fix the errors above or use --skip-validation to ignore
```

### Pular Validação

Para pular a validação (não recomendado):

```bash
p2m run --skip-validation
p2m build --target android --skip-validation
```

### Validação Manual

Para validar o código sem executar ou compilar:

```python
from p2m.core.validator import CodeValidator

validator = CodeValidator()

# Validar um arquivo específico
is_valid, errors, warnings = validator.validate_file("main.py")
validator.print_report(is_valid, errors, warnings)

# Validar todo o projeto
is_valid, errors, warnings = validator.validate_project(".")
validator.print_report(is_valid, errors, warnings)
```

---

## 📊 Tipos de Mensagens

### ❌ Erros
Impedem a execução ou compilação do código. Devem ser corrigidos antes de prosseguir.

Exemplo:
```
main.py:0:0 [ERROR] Missing required function: create_view()
```

### ⚠️ Avisos
Indicam problemas potenciais ou desvios das melhores práticas, mas não impedem a execução.

Exemplo:
```
main.py:1:0 [WARNING] Missing P2M core import (from p2m.core import Render)
```

---

## 📝 Exemplo de Código Válido

```python
from p2m.core import Render
from p2m.ui import Container, Text, Button

def on_click():
    print("Button clicked!")

def create_view():
    container = Container(class_="bg-white p-4")
    text = Text("Hello World")
    button = Button("Click Me", on_click=on_click)
    
    container.add(text).add(button)
    return container.build()  # ✅ Retorna .build()

def main():
    Render.execute(create_view)  # ✅ Chama Render.execute()

if __name__ == "__main__":
    main()
```

---

## 🔧 Troubleshooting

### Erro: "Missing required function: create_view()"

**Solução:** Adicione a função `create_view()` ao seu código:

```python
def create_view():
    container = Container()
    # ... adicione componentes ...
    return container.build()
```

### Erro: "Missing required function: main()"

**Solução:** Adicione a função `main()` ao seu código:

```python
def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()
```

### Aviso: "Missing P2M core import"

**Solução:** Adicione o import no início do arquivo:

```python
from p2m.core import Render
```

### Aviso: "create_view should return component.build()"

**Solução:** Certifique-se de que `create_view()` retorna `.build()`:

```python
def create_view():
    container = Container()
    # ... adicione componentes ...
    return container.build()  # ✅ Correto
```

---

## 📚 Conclusão

O sistema de validação do P2M ajuda a garantir que seu código está correto e segue as melhores práticas. Use-o para identificar e corrigir erros rapidamente, resultando em aplicações mais confiáveis e de melhor qualidade.
