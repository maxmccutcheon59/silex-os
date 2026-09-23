from silex.wedge import KITTING_STEPS, build_kitting_cell


def run_demo(*, fail_quality: bool = False) -> None:
    graph, ledger, runtime, issuer, actor = build_kitting_cell(quality_pass=not fail_quality)
    job = runtime.submit("kit order-1", KITTING_STEPS)
    writ = issuer.issue(actor.id, KITTING_STEPS, "order-1")
    runtime.run(job, writ)
    print(f"status   {job.status.value}")
    print(f"reason   {job.reason}")
    print(f"ledger   {len(ledger.entries)} entries chain_ok={ledger.verify()}")
    print(f"order    {graph.get('order-1').attrs}")
    print(f"cell     {graph.get('cell-1').attrs}")


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
