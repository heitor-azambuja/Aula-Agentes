from pathlib import Path


def test_readme_documents_calculator_usage_api_and_financial_assumptions():
    readme = Path("README.md").read_text(encoding="utf-8")

    required_sections = [
        "## Executando a aplicação",
        "## Regras da simulação financeira",
        "## API",
        "POST /api/simulate",
        "taxa_mensal = (1 + taxa_anual) ** (1 / 12) - 1",
        "saldo inicial do mês → aporte mensal → retiradas → juros",
        "python run.py",
        "curl",
    ]

    missing = [section for section in required_sections if section not in readme]
    assert missing == []
