from app.services.sentinel import check_policy, verify

def test_policy_blocks_low_confidence():
    result = check_policy({
        "confidence": 0.80,
        "action_value": 1000,
        "high_risk": False,
        "auto_actions_enabled": True,
        "minimum_confidence": 0.90,
        "maximum_automatic_action_value": 10000,
    })
    assert result["approved"] is False

def test_policy_approves_safe_action():
    result = check_policy({
        "confidence": 0.92,
        "action_value": 5000,
        "high_risk": False,
        "auto_actions_enabled": True,
        "minimum_confidence": 0.90,
        "maximum_automatic_action_value": 10000,
    })
    assert result["approved"] is True

def test_verification():
    result = verify({
        "before_success_rate": 91.2,
        "after_success_rate": 97.1,
        "expected_after_success_rate": 97.1,
        "tolerance": 0.5,
    })
    assert result["verified"] is True
