"""Recompute ASCENSION's valuation scenarios using only the adjacent inputs."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def dcf(revenue, growth, margins, discount, terminal_growth):
    """Return operating value and discounted terminal value share."""
    flows = []
    for rate, margin in zip(growth, margins, strict=True):
        revenue *= 1 + rate
        flows.append(revenue * margin)
    periods = len(flows)
    terminal = flows[-1] * (1 + terminal_growth) / (discount - terminal_growth)
    terminal_pv = terminal / (1 + discount) ** periods
    value = sum(flow / (1 + discount) ** year
                for year, flow in enumerate(flows, 1)) + terminal_pv
    return value, terminal_pv / value


def main():
    with (HERE / "nvidia-quarterly.csv").open(encoding="utf-8", newline="") as file:
        quarters = list(csv.DictReader(file))
    for quarter in quarters:
        cfo, purchases, principal, reported = (
            float(quarter[key]) for key in
            ("cfo_usd_bn", "purchases_usd_bn", "principal_usd_bn", "reported_fcf_usd_bn")
        )
        assert abs(cfo - purchases - principal - reported) < 1e-8

    inputs = json.loads((HERE / "valuation.json").read_text(encoding="utf-8"))
    nvda = inputs["nvidia"]
    shares = nvda["shares_bn"]
    cap = nvda["price_usd"] * shares
    net_liquid_assets = (nvda["cash_usd_bn"] + nvda["marketable_debt_securities_usd_bn"]
                         + nvda["marketable_equity_usd_bn"] - nvda["debt_usd_bn"])
    ev = cap - net_liquid_assets
    revenue, net_income, cash_flow = (
        sum(float(q[key]) for q in quarters[-4:]) for key in
        ("revenue_usd_bn", "gaap_net_income_usd_bn", "reported_fcf_usd_bn")
    )
    print(f"NVDA LTM sales {revenue:.3f}, net income {net_income:.3f}, FCF {cash_flow:.3f}")
    print(f"NVDA cash bridge {net_liquid_assets:.3f}, cap {cap:.2f}, EV {ev:.2f}, "
          f"P/E {cap/net_income:.2f}x, EV/FCF proxy {ev/cash_flow:.2f}x (USD bn)")
    for scenario in nvda["scenarios"]:
        value, terminal_weight = dcf(revenue, scenario["growth"], scenario["cash_margin"],
                                     scenario["discount"], scenario["terminal_growth"])
        print(f'{scenario["case"]}: operating EV {value:.2f} USD bn, '
              f'equity per share ${(value + net_liquid_assets)/shares:.2f}, '
              f'terminal {terminal_weight:.1%}')
    base = nvda["scenarios"][1]
    discount, terminal_growth = base["discount"], base["terminal_growth"]
    print("NVDA fixed growth implied by observed EV, and base growth sensitivity:")
    for margin in (0.30, 0.36, 0.42):
        low, high = 0.0, 1.0
        for _ in range(40):
            mid = (low + high) / 2
            if dcf(revenue, [mid] * 5, [margin] * 5, discount, terminal_growth)[0] < ev:
                low = mid
            else:
                high = mid
        sensitivity = [
            (dcf(revenue, base["growth"], [margin] * 5, rate, terminal_growth)[0]
             + net_liquid_assets) / shares for rate in (0.095, 0.105, 0.115)
        ]
        print(f"  margin {margin:.0%}: growth {mid:.1%}, "
              f"price at 9.5/10.5/11.5% discount {[round(value, 2) for value in sensitivity]}")
    assert abs(dcf(100, [0], [0.10], 0.10, 0)[0] - 100) < 1e-8

    ant = inputs["anthropic"]
    sales = ant["fy25_revenue_usd_bn"] - ant["ytd25_revenue_usd_bn"] + ant["ytd26_revenue_usd_bn"]
    market_cap = ant["as_if_shares_bn"] * ant["price_usd"]
    print(f"ANT cap {market_cap:.2f} USD bn on prospectus share basis, "
          f"LTM sales {sales:.3f}, P/S {market_cap/sales:.2f}x, "
          f'offer cap {ant["as_if_shares_bn"] * ant["offer_price_usd"]:.2f} USD bn')
    print(f'ANT IPO issuer gross {ant["primary_ipo_shares_bn"] * ant["offer_price_usd"]:.2f}, '
          f'secondary gross {ant["secondary_ipo_shares_bn"] * ant["offer_price_usd"]:.2f}, '
          f'placement gross {ant["private_placement_shares_bn"] * ant["offer_price_usd"]:.2f} USD bn')
    for margin in (0.15, 0.25, 0.35):
        required_sales = market_cap * 0.04 / margin
        print(f"  At {margin:.0%} FCFE margin, 4% equity FCF yield on current price "
              f"requires year-3 sales {required_sales:.2f} USD bn "
              f"({(required_sales/sales)**(1/3)-1:.1%} 3y CAGR).")


if __name__ == "__main__":
    main()
