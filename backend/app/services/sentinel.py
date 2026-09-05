from datetime import datetime, timezone


def _exposure(req, success_rate=None):
    """
    Estimate one hour of revenue exposure caused by payment failures.

    This is a decision-support estimate, not a guaranteed financial loss.
    """
    success_rate = (
        req["payment_success_rate"]
        if success_rate is None
        else success_rate
    )

    failure_rate = max(100 - success_rate, 0) / 100
    hourly_gmv = (
        req["transactions_per_hour"]
        * req["average_order_value"]
    )

    return round(hourly_gmv * failure_rate, 2)


def analyze(req):
    degradation = (
        req["baseline_success_rate"]
        - req["payment_success_rate"]
    )

    exposure = _exposure(req)

    # Simple MVP probability model.
    # In a production system this would be replaced by a trained model.
    probability = min(
        0.99,
        max(0.50, 0.70 + degradation * 0.055)
    )

    evidence = [
        {
            "factor": "UPI",
            "change_pct": 16.2,
            "signal": "failure concentration increased"
        },
        {
            "factor": "Bank-A",
            "change_pct": 31.0,
            "signal": "failure concentration increased"
        },
        {
            "factor": "Mobile",
            "change_pct": 14.0,
            "signal": "failure concentration increased"
        },
        {
            "factor": "Returning users",
            "change_pct": 11.8,
            "signal": "failure concentration increased"
        },
    ]

    return {
        "merchant": req["merchant"],
        "status": (
            "degradation_detected"
            if degradation > 1
            else "normal"
        ),
        "baseline_success_rate": req["baseline_success_rate"],
        "current_success_rate": req["payment_success_rate"],
        "degradation_points": round(degradation, 2),
        "continued_disruption_probability": round(
            probability,
            2
        ),
        "estimated_revenue_exposure": exposure,
        "evidence": evidence,
        "note": (
            "All financial figures are estimates for "
            "decision support, not guaranteed losses."
        ),
    }


def simulate(req):
    """
    Digital Twin:
    evaluate multiple permitted interventions by modeling
    their expected success-rate improvement and resulting
    revenue exposure.
    """

    analysis = analyze(req)
    current_rate = req["payment_success_rate"]

    # Modeled outcomes for the MVP.
    # These represent simulated intervention effects,
    # not live payment-network changes.
    intervention_a_rate = min(
        99.9,
        current_rate + 5.9
    )

    intervention_b_rate = min(
        99.9,
        current_rate + 4.0
    )

    scenarios = [
        {
            "scenario": "Do nothing",
            "simulated_success_rate": round(current_rate, 2),
            "estimated_exposure": _exposure(
                req,
                current_rate
            ),
            "recommended": False,
        },
        {
            "scenario": "Intervention A",
            "simulated_success_rate": round(
                intervention_a_rate,
                2
            ),
            "estimated_exposure": _exposure(
                req,
                intervention_a_rate
            ),
            "recommended": False,
        },
        {
            "scenario": "Intervention B",
            "simulated_success_rate": round(
                intervention_b_rate,
                2
            ),
            "estimated_exposure": _exposure(
                req,
                intervention_b_rate
            ),
            "recommended": False,
        },
    ]

    # Choose the scenario with the lowest simulated exposure.
    recommended_scenario = min(
        scenarios,
        key=lambda scenario: scenario["estimated_exposure"]
    )

    for scenario in scenarios:
        scenario["recommended"] = (
            scenario["scenario"]
            == recommended_scenario["scenario"]
        )

    return {
        "digital_twin": {
            "merchant": req["merchant"],
            "state": "payment_degradation",
            "current_success_rate": current_rate,
        },
        "scenarios": scenarios,
        "recommendation": recommended_scenario["scenario"],
        "reason": (
            "Lowest estimated exposure among the "
            "simulated permitted scenarios."
        ),
    }


def check_policy(req):
    """
    Deterministic policy engine.

    The AI may recommend an action, but policy determines
    whether that action is allowed.
    """

    reasons = []
    approved = True

    if req["confidence"] < req["minimum_confidence"]:
        approved = False
        reasons.append(
            "Confidence below minimum threshold."
        )

    if (
        req["action_value"]
        > req["maximum_automatic_action_value"]
    ):
        approved = False
        reasons.append(
            "Action value exceeds automatic-action limit."
        )

    if req["high_risk"]:
        approved = False
        reasons.append(
            "High-risk transaction category cannot "
            "be auto-executed."
        )

    if not req["auto_actions_enabled"]:
        approved = False
        reasons.append(
            "Merchant has disabled automatic actions."
        )

    return {
        "approved": approved,
        "reasons": (
            reasons
            or ["All configured policy checks passed."]
        ),
        "principle": (
            "AI proposes. Policy controls. "
            "Software executes."
        ),
    }


def execute(req):
    """
    Execute only after deterministic policy approval.

    The current MVP deliberately uses controlled simulation
    rather than claiming to modify live payment routing.
    """

    if not req["approved"]:
        return {
            "executed": False,
            "action": req["action"],
            "message": (
                "Execution blocked because policy "
                "approval was not granted."
            ),
        }

    return {
        "executed": True,
        "action": req["action"],
        "merchant": req["merchant"],
        "execution_mode": "controlled_simulation",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }


def verify(req):
    """
    Verify whether the modeled outcome falls within
    the expected tolerance.
    """

    delta = (
        req["after_success_rate"]
        - req["before_success_rate"]
    )

    passed = (
        abs(
            req["after_success_rate"]
            - req["expected_after_success_rate"]
        )
        <= req["tolerance"]
    )

    return {
        "verified": passed,
        "before_success_rate": (
            req["before_success_rate"]
        ),
        "after_success_rate": (
            req["after_success_rate"]
        ),
        "improvement_points": round(delta, 2),
        "message": (
            "Outcome verified"
            if passed
            else "Outcome did not meet "
                 "verification tolerance."
        ),
    }


def novakart_demo():
    """
    Complete Sentinel closed-loop demonstration.

    Observe → Predict → Quantify → Explain →
    Simulate → Decide → Policy Check → Act →
    Verify → Audit
    """

    req = {
        "merchant": "NovaKart",
        "payment_success_rate": 91.2,
        "baseline_success_rate": 97.8,
        "transactions_per_hour": 1200,
        "average_order_value": 1850,
    }

    # 1. Observe / Predict / Quantify / Explain
    analysis = analyze(req)

    # 2. Digital Twin simulation
    simulation = simulate(req)

    # 3. Decision
    recommended_action = simulation["recommendation"]

    # 4. Deterministic policy validation
    policy = check_policy({
        "confidence": analysis[
            "continued_disruption_probability"
        ],
        "action_value": 5000,
        "high_risk": False,
        "auto_actions_enabled": True,
        "minimum_confidence": 0.90,
        "maximum_automatic_action_value": 10000,
    })

    # 5. Controlled execution
    execution = execute({
        "approved": policy["approved"],
        "action": recommended_action,
        "merchant": "NovaKart",
    })

    # 6. Verify modeled result
    selected_scenario = next(
        scenario
        for scenario in simulation["scenarios"]
        if scenario["scenario"] == recommended_action
    )

    verification = verify({
        "before_success_rate": req[
            "payment_success_rate"
        ],
        "after_success_rate": selected_scenario[
            "simulated_success_rate"
        ],
        "expected_after_success_rate": selected_scenario[
            "simulated_success_rate"
        ],
        "tolerance": 0.5,
    })

    # 7. Audit
    audit = {
        "event": "payment_degradation_response",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "stages_completed": [
            "observe",
            "predict",
            "quantify",
            "explain",
            "simulate",
            "decide",
            "policy_check",
            "act",
            "verify",
            "audit",
        ],
    }

    return {
        "demo": "NovaKart payment degradation",
        "analysis": analysis,
        "simulation": simulation,
        "policy": policy,
        "execution": execution,
        "verification": verification,
        "audit": audit,
    }
