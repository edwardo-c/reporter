from utils.yaml_loader import load_yaml
from config.paths import PRICE_LIST_YAML
from pathlib import Path

def test_env_interpolation(tmp_path, monkeypatch):
    # Arrange
    plan = """
imports:
  all:
    - op: dir_to_csv
      args:
        dir: ${PRICE_GROUPS_DIR}
"""
    f = tmp_path / "config.yaml"
    f.write_text(plan, encoding="utf-8")
    monkeypatch.setenv("PRICE_GROUPS_DIR", "/tmp/pg")

    # Act
    cfg = load_yaml(f)

    # Assert
    assert cfg["imports"]["all"][0]["args"]["dir"] == "/tmp/pg"
