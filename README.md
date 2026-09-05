# 🛡️ Sentinel — AI Business Autopilot

> **Predict problems. Quantify impact. Simulate decisions. Act safely. Verify outcomes.**

Sentinel is a predictive merchant decision-and-action layer that helps businesses detect revenue-impacting problems before they become major losses.

Instead of waiting for a merchant to discover that payments, checkout, subscriptions, or other business signals have deteriorated, Sentinel continuously analyzes operational signals, predicts what may happen next, estimates financial exposure, evaluates possible interventions, validates the recommended action against deterministic policies, and verifies the result.

---

## 🚨 The Problem

Most merchant and payment systems are reactive.

A typical workflow looks like:

**Problem occurs → Merchant notices → Team investigates → Team decides → Action is taken**

By the time the problem is discovered, revenue may already have been lost.

Sentinel changes the workflow to:

**Observe → Predict → Quantify → Explain → Simulate → Decide → Policy Check → Act → Verify → Audit**

The goal is not simply to detect an anomaly.

The goal is to answer:

> **"What is likely to happen, how much could it matter, what should we do, and are we allowed to do it?"**

---

# 💡 What Sentinel Does

Sentinel combines predictive analytics, financial impact estimation, simulation, deterministic policies, and controlled execution.

### 1. Observe

Detect abnormal changes in merchant signals.

Example:

- Baseline payment success rate: **97.8%**
- Current payment success rate: **91.2%**
- Degradation: **6.6 percentage points**

---

### 2. Predict

Estimate the probability that the disruption will continue.

Current NovaKart demo:

**99% continued-disruption probability**

> The current probability model is an MVP demonstration model. A production system would use a trained model on historical merchant data.

---

### 3. Quantify

Translate operational degradation into an estimated financial exposure.

The MVP estimates one-hour revenue exposure using:

**Affected transaction volume × failure rate × average order value**

For the NovaKart demonstration:

**Estimated exposure: ₹1,95,360**

This is a decision-support estimate, not a guaranteed financial loss.

---

### 4. Explain

Sentinel surfaces evidence associated with the degradation.

Example signals:

| Signal | Change |
|---|---:|
| UPI | +16.2% |
| Bank-A | +31.0% |
| Mobile | +14.0% |
| Returning users | +11.8% |

These signals help the merchant understand **why Sentinel believes the problem matters**.

---

### 5. Simulate

Sentinel uses a Digital Twin-style simulation to compare possible outcomes before taking action.

For NovaKart:

| Scenario | Simulated Success Rate | Estimated Exposure |
|---|---:|---:|
| Do nothing | 91.2% | ₹1,95,360 |
| Intervention A | 97.1% | ₹64,380 |
| Intervention B | 95.2% | ₹1,06,560 |

The system selects:

### ✅ Intervention A

because it produces the lowest modeled exposure among the simulated permitted scenarios.

> These are modeled outcomes in the MVP, not claims of live payment-network changes.

---

# 🔐 Policy Engine

Sentinel does **not** allow an AI model to directly control business actions.

The architecture separates intelligence from authority.

### AI / Intelligence Layer

AI can:

- analyze signals
- predict outcomes
- explain evidence
- recommend actions
- compare scenarios

### Deterministic Policy Layer

Software decides whether an action is allowed based on:

- confidence threshold
- action-value limit
- risk level
- merchant automation settings

For example:

```text
Confidence ≥ minimum threshold
AND
Action value ≤ automatic-action limit
AND
High-risk = false
AND
Automatic actions = enabled
