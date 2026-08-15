# Ledger 0014 — Adversarial self-review (red-team of the RESEARCH PROCESS itself)

**Date:** 2026-08-15 · Requested by project owner: rate the work, then attack it as a hostile critic, then find the best path.

---

## PART 1 — The defense (my honest rating)

| Dimension | Score | Basis |
|---|---|---|
| Holdout discipline | 9/10 | every holdout touched once; failures published verbatim |
| Data engineering | 7/10 | validated, cross-checked, self-acquired intraday |
| Statistical honesty | 7/10 | bootstrap CIs, trial accounting, disclosed contaminations |
| Breadth of ideas | 5/10 | 3 mechanism families + 1 pending; all "known classics" |
| Deliverable value | 6/10 | trustworthy null result + working stack; no deployable strategy |
| **Overall** | **6.8/10** | a clean lab that has so far proven only negatives |

## PART 2 — The prosecution (opposing counsel attacks)

**Attack 1 — "Your null result is weaker than you claim."**
You tested LONG-ONLY, DAILY-BAR, RETAIL-COST crypto. That's one corner of strategy space. No shorts, no pairs/spread trades, no cross-exchange arbitrage, no order-book signals, no funding-rate harvesting. Calling the program "closed" overstated the evidence. *Verdict: partially GUILTY — the FINAL_REPORT scoped it correctly, but my chat summaries sometimes said "everything failed" without the qualifiers.*

**Attack 2 — "Single-source data risk."**
The new hourly file comes from one exchange (Bitstamp) via two intermediaries (Kaggle → a stranger's GitHub repo). You cross-checked closes against CoinMetrics (0.4% median) — good — but wicks/highs/lows are UNVERIFIED against any second source, and 4A/4C decisions depend precisely on wicks. *Verdict: GUILTY. Mitigation required: verify H/L against Kraken's native OHLC for the overlapping period before trusting 4A/4C results.*

**Attack 3 — "Survivorship in your universe."**
BTC/ETH/LTC/XRP/DOGE/ADA/BNB are coins that SURVIVED to 2026. A rotation strategy tested only on survivors gets inflated results — dead coins (LUNA, FTT...) are exactly what rotation would have bought on the way down. *Verdict: GUILTY, but note direction: survivorship bias INFLATES backtests, and rotation failed anyway — the true result is even worse. Null conclusions are strengthened, not weakened. Still, this must be stated.*

**Attack 4 — "Your paper-trading 'success' is cherry-picked framing."**
"-6.4% vs -18.5%" sounds great but a strategy REJECTED at TEST is being showcased with 82 bars of favorable regime. That's the exact behavior the package warns about. *Verdict: GUILTY as framed in chat (I did label it 'not evidence', but showcasing it at all invites the wrong conclusion). Correction: report it neutrally or not at all.*

**Attack 5 — "The 2 CPU sandbox shapes your conclusions."**
You concluded "no edge at daily bars" partly because that's all the compute/data you had. A real shop would test tick data, order books, hundreds of instruments. *Verdict: TRUE but not actionable here; the conclusion is honest WITHIN its stated scope.*

**Attack 6 — "Speed."**
Families 2R and 3B were pre-registered and executed same-day by the same agent. Pre-registration's power comes from separation between designer and evaluator; here both are me, minutes apart. The protection is real (frozen text, no grid) but weaker than it looks. *Verdict: fair point; unavoidable for a solo agent; disclosed now.*

## PART 3 — The ruling: what actually changes

1. **Before ANY 4A/4C run:** verify hourly High/Low quality against Kraken native candles (720-bar overlap window). If wicks disagree materially → 4A/4C results get a low-trust flag regardless of outcome.
2. FINAL_REPORT gets a scope-limitation paragraph (long-only, survivors-only universe, single venue).
3. Paper-trading reports switch to neutral framing.
4. Family 4 proceeds — it remains the best pre-registered use of genuinely new data.

## PART 4 — Is there a better path beyond all these ideas?

Ranked by (value × probability × feasibility), the honest top-3 beyond Family 4:

**Path A — Funding-rate / carry harvesting (NEW mechanism class, undertested).**
Perpetual futures pay periodic funding between longs and shorts. Harvesting it is an *income* mechanism (like collecting rent), not a *prediction* mechanism — structurally different from everything we falsified. Public funding-rate history exists (exchange APIs/GitHub mirrors). Realistic, documented, and the first idea whose edge source isn't "guess the direction". **This is the best next research idea if data can be acquired.**

**Path B — The discipline/guardian product (engineering, not research).**
Stop seeking alpha; ship what's already validated: the risk-engine + vol-scaling wrapper as a "protect me from myself" bot on a demo account. Its claim (fewer catastrophic drawdowns than emotional trading) is supported by everything we measured. Highest probability of delivering something USABLE.

**Path C — Accept completion.** The project already produced its scientifically valid deliverable. Stopping is legitimate.

## PART 5 — Attack 2 mitigation executed (same day)

Wick verification vs an independent source (CryptoCompare hourly, read via LFS route):
- Raw comparison showed alarming 3-6% wick divergence → investigated instead of ignored.
- Lag scan revealed the divergence minimizes at a **+4h shift (0.26% vs 4.19% at zero lag)** — a timestamp-alignment artifact in the comparison, not price disagreement.
- Decisive test on OUR file: across **3,910 overlapping days**, Bitstamp daily closes vs validated CoinMetrics: **median 0.44% as-is vs 0.71% when shifted +4h** → our file's UTC timestamps are correct; the second source (or its export) carries the offset.
- Internal wick sanity: 0 OHLC violations in 93,822 candles.

**Verdict:** primary dataset upgraded to trusted for close-based work; wicks corroborated indirectly (correct alignment + internal consistency) but never matched candle-by-candle against a second source — 4A/4C conclusions will carry a stated single-venue-wicks caveat. Attack 2: addressed as far as available data allows.

## FINAL RECOMMENDATION (ruling + Part 4 combined)
Family 4 now (pre-registered, wick caveat attached) → Path A (funding-rate carry) if data proves acquirable → Path B (discipline/guardian bot) as the shipping goal regardless of research outcomes. Path C (accept completion) stays on the table.
