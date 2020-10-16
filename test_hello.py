from click.testing import CliRunner
from hello import calculate


def test_calculate():
    runner = CliRunner()
    result = runner.invoke(calculate, ["--value1", "1", "--value2", "2"])
    assert result.exit_code == 0
    assert "2" in result.output
