"""
Code (line) coverage tests for event_ticket_tier.py
Goal: execute every line of the application at least once.
"""
import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


# ---------- process_ticket_manifest ----------

def test_single_general_order():
    # Original example test: 2 x 45 = 90, +10% tax = 99.0
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "exclusive_lounge": False,
        "orders": [{"qty": 2, "promo": ""}],
    }]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"


def test_invalid_manifests_type_raises():
    # Line 3: manifests is not a list
    with pytest.raises(ValueError):
        process_ticket_manifest("not a list", 0.1)


def test_unconfirmed_manifest_is_skipped():
    # Line 10: unconfirmed manifest is ignored, only the confirmed one counts
    manifests = [
        {"is_confirmed": False, "tier": "vip", "orders": [{"qty": 10, "promo": ""}]},
        {"is_confirmed": True, "tier": "general", "orders": [{"qty": 2, "promo": ""}]},
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {"total_revenue": 99.0, "status": "COMPLETED"}


def test_vip_tier_price():
    # Line 16: VIP base price 150, qty 1, +10% tax = 165.0
    manifests = [{"is_confirmed": True, "tier": "vip", "orders": [{"qty": 1, "promo": ""}]}]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {"total_revenue": 165.0, "status": "COMPLETED"}


def test_premium_tier_with_earlybird():
    # Lines 18 and 43: premium 2 x 90 = 180, EARLYBIRD 20% off = 144.0
    manifests = [{"is_confirmed": True, "tier": "premium", "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}]
    result = process_ticket_manifest(manifests, 0.0)
    assert result == {"total_revenue": 144.0, "status": "COMPLETED"}


def test_unknown_tier_is_rejected():
    # Lines 22-23: unknown tier counts as a rejection, nothing billed
    manifests = [{"is_confirmed": True, "tier": "platinum", "orders": [{"qty": 1, "promo": ""}]}]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_zero_quantity_order_is_rejected():
    # Lines 32-33: qty <= 0 is rejected, the valid order is still billed
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 0, "promo": ""}, {"qty": 1, "promo": ""}],
    }]
    result = process_ticket_manifest(manifests, 0.0)
    assert result == {"total_revenue": 45.0, "status": "COMPLETED"}


def test_vip_fraud_risk_voids_manifest():
    # Lines 38-41: FRAUD_RISK on VIP wipes the manifest and stops processing its orders
    manifests = [{
        "is_confirmed": True,
        "tier": "vip",
        "orders": [{"qty": 2, "promo": "FRAUD_RISK"}, {"qty": 1, "promo": ""}],
    }]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_bulk_discount_for_five_or_more():
    # Line 46: 5 x 45 = 225, bulk discount -20 = 205.0
    manifests = [{"is_confirmed": True, "tier": "general", "orders": [{"qty": 5, "promo": ""}]}]
    result = process_ticket_manifest(manifests, 0.0)
    assert result == {"total_revenue": 205.0, "status": "COMPLETED"}


def test_exclusive_lounge_surcharge():
    # Line 51: 45 + 75 lounge fee = 120.0
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "exclusive_lounge": True,
        "orders": [{"qty": 1, "promo": ""}],
    }]
    result = process_ticket_manifest(manifests, 0.0)
    assert result == {"total_revenue": 120.0, "status": "COMPLETED"}


def test_audit_rejected_when_more_than_four_rejections():
    # Line 58: five rejected orders -> AUDIT_REJECTED
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 0, "promo": ""}] * 5,
    }]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["status"] == "AUDIT_REJECTED"


def test_empty_manifest_list_is_zero_sales():
    # Line 60: nothing to process -> ZERO_SALES
    result = process_ticket_manifest([], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- monitor_gate_flow ----------

def test_gate_flow_no_data():
    # Lines 65-66
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_flow_overflow():
    # Lines 71-74: two consecutive rates above 50
    assert monitor_gate_flow([[60, 70]]) == "OVERFLOW"


def test_gate_flow_normal_with_streak_reset():
    # Lines 75-77: a low rate resets the streak, so no overflow
    assert monitor_gate_flow([[60, 10, 60]]) == "FLOW_NORMAL"
