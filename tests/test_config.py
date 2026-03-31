"""配置測試"""
import pytest
from pathlib import Path
import tempfile
import shutil

# 測試前設定
@pytest.fixture
def temp_workspace():
    """建立臨時工作區"""
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp)

# 測試 Config
def test_config_init(temp_workspace):
    """測試配置初始化"""
    from src.core.config import Config
    config = Config(temp_workspace)
    assert config.workspace == temp_workspace

def test_get_team_dir(temp_workspace):
    """測試取得團隊目錄"""
    from src.core.config import Config
    config = Config(temp_workspace)
    team_dir = config.get_team_dir("test-team")
    assert team_dir.exists()
    assert team_dir.name == "test-team"

def test_save_and_load_state(temp_workspace):
    """測試狀態儲存"""
    from src.core.config import Config
    config = Config(temp_workspace)
    state = {"name": "test", "agents": []}
    config.save_state("test", state)
    loaded = config.load_state("test")
    assert loaded["name"] == "test"

def test_list_teams(temp_workspace):
    """測試列出團隊"""
    from src.core.config import Config
    config = Config(temp_workspace)
    config.save_state("team1", {"name": "team1"})
    config.save_state("team2", {"name": "team2"})
    teams = config.list_teams()
    assert "team1" in teams
    assert "team2" in teams
