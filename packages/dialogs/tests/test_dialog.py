import time
import pytest
from RPA.Dialogs.dialog import Dialog

ELEMENTS = []


@pytest.fixture
def dialog():
    d = Dialog(
        elements=ELEMENTS,
        title="Test title",
        width=640,
        height=480,
        on_top=False,
        debug=False,
    )
    try:
        yield d
    finally:
        if d.is_started:
            d.stop()


def test_not_started(dialog):
    assert not dialog.is_started

    with pytest.raises(RuntimeError):
        dialog.stop()

    with pytest.raises(RuntimeError):
        dialog.poll()

    with pytest.raises(RuntimeError):
        dialog.wait()

    with pytest.raises(RuntimeError):
        dialog.result()


def test_start(dialog):
    dialog.start()

    end = time.time() + 5
    while time.time() <= end:
        assert not dialog.poll()


def test_stop(dialog):
    dialog.start()
    dialog.stop()

    with pytest.raises(RuntimeError) as err:
        dialog.result()

    assert str(err.value) == "Stopped by execution"

    # Second stop() should not raise
    dialog.stop()
