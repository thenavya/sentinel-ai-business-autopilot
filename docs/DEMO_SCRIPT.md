# 5-minute Sentinel demo

## 0:00–0:30 — Problem
“Traditional merchant dashboards are reactive. They show that payment performance dropped, but the merchant still has to investigate, estimate the financial impact, decide what to do, and verify whether it worked.”

## 0:30–1:15 — NovaKart incident
Show:
- Baseline: 97.8%
- Current: 91.2%
- 1,200 transactions/hour
- AOV: ₹1,850

Say:
“Sentinel detects the deviation from NovaKart's baseline.”

## 1:15–2:00 — Predict + quantify + explain
Show:
- 92–94% continued-disruption probability
- Estimated exposure
- UPI, Bank-A, Mobile, returning-user evidence

Say:
“The probability is an estimate, not a claim that the AI knows the future. The root-cause explanation is grounded in structured evidence.”

## 2:00–3:00 — Digital Twin / What-if
Show:
- Do nothing
- Intervention A
- Intervention B

Say:
“Sentinel doesn't jump straight from detection to action. It simulates alternatives and compares expected outcomes.”

## 3:00–3:45 — Policy
Show:
- Confidence ≥ 90%
- Auto action value ≤ ₹10,000
- High-risk = never auto-act
- Auto actions enabled

Say:
“The LLM cannot bypass this layer. Policy is deterministic.”

## 3:45–4:30 — Execute + verify
Show:
- Approved
- Controlled simulation execution
- 91.2% → 97.1%
- Outcome verified

## 4:30–5:00 — Audit
Show event history and finish:
“Sentinel is not another dashboard or chatbot. It is a predictive decision-and-action layer with constrained autonomy and verification.”
