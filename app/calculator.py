"""Motor de cálculo da calculadora de juros compostos."""

from __future__ import annotations

from typing import Any


def _monthly_rate_from_effective_annual_rate(annual_interest_rate: float) -> float:
    """Converte taxa anual efetiva percentual em taxa mensal composta."""
    return (1 + annual_interest_rate / 100) ** (1 / 12) - 1


def _money(value: float) -> float:
    """Arredonda valores monetários para duas casas decimais."""
    return round(value + 0, 2)


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
