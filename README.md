# Aula-Agentes

Repositório de apoio para aulas e experimentos sobre agentes de IA. O projeto atual contém uma calculadora web de juros compostos com backend Flask, frontend Dash/Plotly e testes automatizados em Python.

## Objetivo

Permitir que uma pessoa simule a evolução de um investimento considerando:

- aporte inicial;
- tempo de investimento;
- taxa de juros anual efetiva;
- aportes mensais;
- retiradas pontuais;
- retiradas recorrentes.

A aplicação retorna o saldo final, o total aportado, o total retirado, os juros acumulados, uma série mensal detalhada e um gráfico de evolução do patrimônio.

## Pré-requisitos

- Python 3.11 ou superior.
- `pip` para instalar dependências.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/heitor-azambuja/Aula-Agentes.git
cd Aula-Agentes
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Executando a aplicação

Suba o servidor integrado Flask + Dash:

```bash
python run.py
```

Depois acesse:

```text
http://localhost:8050/dashboard/
```

A API permanece disponível no mesmo servidor em `/api/simulate`.

## Verificação local

Rode os testes:

```bash
python -m pytest
```

Rode o lint:

```bash
python -m ruff check .
```

Valide tudo localmente:

```bash
make check
```

## Regras da simulação financeira

A taxa informada pelo usuário é interpretada como taxa anual efetiva em percentual. Internamente, ela é convertida para taxa mensal composta usando:

```text
taxa_mensal = (1 + taxa_anual) ** (1 / 12) - 1
```

Como a entrada da aplicação usa percentual, a implementação converte primeiro `taxa_anual / 100`.

A ordem de cálculo em cada mês é:

```text
saldo inicial do mês → aporte mensal → retiradas → juros
```

Retiradas pontuais são aplicadas no mês informado. Retiradas recorrentes aceitam mês inicial, mês final opcional e periodicidade em meses.

## API

### POST /api/simulate

Exemplo de requisição com `curl`:

```bash
curl -X POST http://localhost:8050/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "initial_amount": 10000,
    "annual_interest_rate": 8,
    "duration_months": 24,
    "monthly_contribution": 500,
    "one_time_withdrawals": [
      {"month": 12, "amount": 1000}
    ],
    "recurring_withdrawals": [
      {"start_month": 18, "end_month": 24, "amount": 200, "frequency_months": 1}
    ]
  }'
```

Campos de entrada:

- `initial_amount`: aporte inicial.
- `annual_interest_rate`: taxa anual efetiva em percentual.
- `duration_months`: tempo de investimento em meses.
- `monthly_contribution`: aporte mensal recorrente.
- `one_time_withdrawals`: lista de retiradas pontuais com `month` e `amount`.
- `recurring_withdrawals`: lista de retiradas recorrentes com `start_month`, `end_month` opcional, `amount` e `frequency_months`.

Exemplo de resposta:

```json
{
  "summary": {
    "final_balance": 23520.42,
    "total_contributed": 22000.0,
    "total_withdrawn": 2400.0,
    "total_interest": 3920.42
  },
  "monthly_records": [
    {
      "month": 1,
      "beginning_balance": 10000.0,
      "contribution": 500.0,
      "withdrawal": 0.0,
      "interest": 67.48,
      "ending_balance": 10567.48
    }
  ]
}
```

Payloads inválidos retornam HTTP 400 com uma mensagem no campo `error`.

## Estrutura do projeto

```text
Aula-Agentes/
├── app/
│   ├── __init__.py
│   ├── api.py          # Aplicação Flask e endpoint HTTP
│   ├── calculator.py   # Motor puro de simulação financeira
│   └── dashboard.py    # Interface Dash/Plotly
├── tests/              # Testes automatizados
├── run.py              # Entrada do servidor integrado
├── requirements.txt
├── pyproject.toml
├── Makefile
├── README.md
└── LICENSE
```

## Contribuição

Para contribuir:

1. Crie uma branch a partir da branch base do projeto.
2. Faça alterações pequenas e bem descritas.
3. Rode `make check` antes de abrir um pull request.
4. Atualize este README sempre que adicionar novos comandos, dependências ou fluxos de uso.
5. Abra um pull request explicando o que foi alterado.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
