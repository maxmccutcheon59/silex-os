from silex.loop import STEPS, build_demo_world


def main() -> None:
    graph, ledger, runtime, issuer = build_demo_world()
    job = runtime.submit("close work order 1", STEPS)
    for step in STEPS:
        writ = issuer.issue(actor="cell-1", action=step, resource="order-1")
        runtime.tick(job, writ)
        print(f"{step:8} -> {job.status.value} {job.reason or ''}")
        if job.status.value == "halted":
            break
    print(f"ledger entries: {len(ledger.entries)}")
    print(f"order: {graph.get('order-1').attrs}")


if __name__ == "__main__":
    main()
