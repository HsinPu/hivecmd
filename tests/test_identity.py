"""身份測試"""
import pytest
from src.core.identity import AgentIdentity

def test_agent_identity_creation():
    """測試建立身份"""
    identity = AgentIdentity(name="test", team="team1", role="worker")
    assert identity.name == "test"
    assert identity.team == "team1"
    assert identity.role == "worker"
    assert identity.status == "idle"

def test_agent_identity_to_dict():
    """測試轉換為字典"""
    identity = AgentIdentity(name="test", team="team1", task="do something")
    data = identity.to_dict()
    assert data["name"] == "test"
    assert data["task"] == "do something"
