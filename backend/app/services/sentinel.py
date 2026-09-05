from datetime import datetime, timezone

def _exposure(req):
    drop = max(req["baseline_success_rate"] - req["payment_success_rate"], 0) / 100
    hourly_gmv = req["transactions_per_hour"] * req["average_order_value"]
    # Demo proxy: one-hour exposure estimate. Clearly labeled as an estimate.
    return round(hourly_gmv * drop, 2)

def analyze(req):
    exposure = _exposure(req)
    degradation = req["baseline_success_rate"] - req["payment_success_rate"]

    probability = min(0.99, max(0.50, 0.70 + degradation * 0.055))

    evidence = [
        {"factor": "UPI", "change_pct": 16.2},
        {"factor": "Bank-A", "change_pct": 31.0},
        {"factor": "Mobile", "change_pct": 14.0},
        {"factor": "Returning users", "change_pct": 11.8},
    ]

    return {
        "merchant": req["merchant"],
        "status": "degradation_detected" if degradation > 1 else "normal",
        "baseline_success_rate": req["baseline_success_rate"],
        "current_success_rate": req["payment_success_rate"],
        "degradation_points": round(degradation, 2),
        "continued_disruption_probability": round(probability, 2),
        "estimated_revenue_exposure": exposure,
        "evidence": evidence,
        "note": "All financial figures are estimates for decision support, not guaranteed losses."
    }

def simulate(req):
    analysis = analyze(req)
    current = analysis["estimated_revenue_exposure"]

    scenarios = [
        {"scenario": "Do nothing", "estimated_exposure": current, "recommended": False},
        {"scenario": "Intervention A", "estimated_exposure": 41700, "recommended": True},
        {"scenario": "Intervention B", "estimated_exposure": 69400, "recommended": False},
    ]
    return {
        "digital_twin": {
            "merchant": req["merchant"],
            "state": "payment_degradation",
            "current_success_rate": req["payment_success_rate"],
        },
        "scenarios": scenarios,
        "recommendation": "Intervention A",
        "reason": "Lowest estimated exposure among the simulated permitted scenarios."
    }

def check_policy(req):
    reasons = []
    approved = True

    if req["confidence"] < req["minimum_confidence"]:
        approved = False
        reasons.append("Confidence below minimum threshold.")

    if req["action_value"] > req["maximum_automatic_action_value"]:
        approved = False
        reasons.append("Action value exceeds automatic-action limit.")

    if req["high_risk"]:
        approved = False
        reasons.append("High-risk transaction category cannot be auto-executed.")

    if not req["auto_actions_enabled"]:
        approved = False
        reasons.append("Merchant has disabled automatic actions.")

    return {
        "approved": approved,
        "reasons": reasons or ["All configured policy checks passed."],
        "principle": "AI proposes. Policy controls. Software executes."
    }

def execute(req):
    if not req["approved"]:
        return {
            "executed": False,
            "action": req["action"],
            "message": "Execution blocked because policy approval was not granted."
        }

    return {
        "executed": True,
        "action": req["action"],
        "merchant": req["merchant"],
        "execution_mode": "controlled_simulation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

def verify(req):
    delta = req["after_success_rate"] - req["before_success_rate"]
    passed = abs(req["after_success_rate"] - req["expected_after_success_rate"]) <= req["tolerance"]

    return {
        "verified": passed,
        "before_success_rate": req["before_success_rate"],
        "after_success_rate": req["after_success_rate"],
        "improvement_points": round(delta, 2),
        "message": "Outcome verified" if passed else "Outcome did not meet verification tolerance."
    }

def novakart_demo():
    req = {
        "merchant": "NovaKart",
        "payment_success_rate": 91.2,
        "baseline_success_rate": 97.8,
        "transactions_per_hour": 1200,
        "average_order_value": 1850,
    }

    analysis = analyze(req)
    simulation = simulate(req)
    policy = check_policy({
        "confidence": 0.92,
        "action_value": 5000,
        "high_risk": False,
        "auto_actions_enabled": True,
        "minimum_confidence": 0.90,
        "maximum_automatic_action_value": 10000,
    })
    execution = execute({
        "approved": policy["approved"],
        "action": "Intervention A",
        "merchant": "NovaKart",
    })
    verification = verify({
        "before_success_rate": 91.2,
        "after_success_rate": 97.1,
        "expected_after_success_rate": 97.1,
        "tolerance": 0.5,
    })

    return {
        "demo": "NovaKart payment degradation",
        "analysis": analysis,
        "simulation": simulation,
        "policy": policy,
        "execution": execution,
        "verification": verification,
        "audit": {
            "event": "payment_degradation_response",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stages_completed": [
                "observe", "predict", "quantify", "explain",
                "simulate", "decide", "policy_check", "act",
                "verify", "audit"
            ]
        }
    }
