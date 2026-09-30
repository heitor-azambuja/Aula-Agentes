"""Motor de cálculo da calculadora de juros compostos."""

from __future__ import annotations

from typing import Any


def _monthly_rate_from_effective_annual_rate(annual_interest_rate: float) -> float:
    """Converte taxa anual efetiva percentual em taxa mensal composta."""
    return (1 + annual_interest_rate / 100) ** (1 / 12) - 1


def _money(value: float) -> float:
    """Arredonda valores monetários para duas casas decimais."""
    return round(value + 0, 2)


def _validate_non_negative(value: float, field_name: str) -> None:
    if float(value) < 0:
        raise ValueError(f"{field_name} deve ser maior ou igual a zero")


def _validate_inputs(
    *,
    initial_amount: float,
    annual_interest_rate: float,
    duration_months: int,
    monthly_contribution: float,
    one_time_withdrawals: list[dict[str, Any]],
    recurring_withdrawals: list[dict[str, Any]],
) -> None:
    _validate_non_negative(initial_amount, "aporte inicial")
    _validate_non_negative(annual_interest_rate, "taxa anual")
    _validate_non_negative(monthly_contribution, "aporte mensal")

    if int(duration_months) <= 0:
        raise ValueError("tempo de investimento deve ser maior que zero")

    for withdrawal in one_time_withdrawals:
        month = int(withdrawal.get("month", 0))
        amount = float(withdrawal.get("amount", 0))
        if month < 1 or month > int(duration_months):
            raise ValueError("retirada pontual fora do período de investimento")
        _validate_non_negative(amount, "valor da retirada pontual")

    for withdrawal in recurring_withdrawals:
        start_month = int(withdrawal.get("start_month", 0))
        end_month = withdrawal.get("end_month")
        amount = float(withdrawal.get("amount", 0))
        frequency_months = int(withdrawal.get("frequency_months", 1))

        if start_month < 1 or start_month > int(duration_months):
            raise ValueError("retirada recorrente fora do período de investimento")
        if end_month is not None and int(end_month) < start_month:
            raise ValueError("mês final da retirada recorrente deve ser após o mês inicial")
        if frequency_months <= 0:
            raise ValueError("periodicidade da retirada recorrente deve ser maior que zero")
        _validate_non_negative(amount, "valor da retirada recorrente")


def _one_time_withdrawal_for_month(
    month: int,
    one_time_withdrawals: list[dict[str, Any]],
) -> float:
    return sum(
        float(withdrawal.get("amount", 0))
        for withdrawal in one_time_withdrawals
        if int(withdrawal.get("month", 0)) == month
    )


def _recurring_withdrawal_for_month(
    month: int,
    recurring_withdrawals: list[dict[str, Any]],
) -> float:
    total = 0.0
    for withdrawal in recurring_withdrawals:
        start_month = int(withdrawal.get("start_month", 1))
        end_month = withdrawal.get("end_month")
        frequency_months = int(withdrawal.get("frequency_months", 1))

        if month < start_month:
            continue
        if end_month is not None and month > int(end_month):
            continue
        if (month - start_month) % frequency_months != 0:
            continue

        total += float(withdrawal.get("amount", 0))
    return total


def _withdrawal_for_month(
    month: int,
    one_time_withdrawals: list[dict[str, Any]],
    recurring_withdrawals: list[dict[str, Any]],
) -> float:
    return _one_time_withdrawal_for_month(
        month,
        one_time_withdrawals,
    ) + _recurring_withdrawal_for_month(month, recurring_withdrawals)


def simulate_compound_interest(
    *,
    initial_amount: float,
    annual_interest_rate: float,
    duration_months: int,
    monthly_contribution: float = 0,
    one_time_withdrawals: list[dict[str, Any]] | None = None,
    recurring_withdrawals: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Simula a evolução mensal de um investimento com juros compostos.

    A taxa anual é interpretada como taxa anual efetiva em percentual. A simulação
    aplica, em cada mês: saldo inicial, aporte mensal, retiradas e juros do mês.
    """
    one_time_withdrawals = one_time_withdrawals or []
    recurring_withdrawals = recurring_withdrawals or []
    _validate_inputs(
        initial_amount=initial_amount,
        annual_interest_rate=annual_interest_rate,
        duration_months=duration_months,
        monthly_contribution=monthly_contribution,
        one_time_withdrawals=one_time_withdrawals,
        recurring_withdrawals=recurring_withdrawals,
    )

    monthly_rate = _monthly_rate_from_effective_annual_rate(annual_interest_rate)
    balance = float(initial_amount)
    total_contributed = float(initial_amount)
    total_withdrawn = 0.0
    total_interest = 0.0
    monthly_records: list[dict[str, float | int]] = []

    for month in range(1, int(duration_months) + 1):
        beginning_balance = balance
        contribution = float(monthly_contribution)
        withdrawal = _withdrawal_for_month(month, one_time_withdrawals, recurring_withdrawals)

        balance += contribution
        total_contributed += contribution
        balance -= withdrawal
        total_withdrawn += withdrawal

        interest = balance * monthly_rate
        balance += interest
        total_interest += interest

        monthly_records.append(
            {
                "month": month,
                "beginning_balance": _money(beginning_balance),
                "contribution": _money(contribution),
                "withdrawal": _money(withdrawal),
                "interest": _money(interest),
                "ending_balance": _money(balance),
            }
        )

    return {
        "summary": {
            "final_balance": _money(balance),
            "total_contributed": _money(total_contributed),
            "total_withdrawn": _money(total_withdrawn),
            "total_interest": _money(total_interest),
        },
        "monthly_records": monthly_records,
    }
