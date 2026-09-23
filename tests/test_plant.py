from silex.plant import Plant
from silex.runtime import Status


def test_console_loop_closes():
    plant = Plant()
    plant.propose("kit order-1")
    plant.submit()
    plant.issue()
    plant.run()
    assert plant.snapshot()["job"]["status"] == Status.CLOSED.value
    assert plant.snapshot()["chain_ok"] is True


def test_propose_cannot_run_without_writ():
    plant = Plant()
    plant.propose("kit order-1")
    plant.submit()
    try:
        plant.tick()
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_quality_halt_from_console():
    plant = Plant()
    plant.set_quality(False)
    plant.submit("kit order-1", plant.snapshot()["allowed_steps"])
    plant.issue()
    plant.run()
    assert plant.snapshot()["job"]["status"] == "halted"
