# Architecture

```
proposer (human | local planner | optional LLM)
        |
        v
   job + policy pack
        |
        v
   writ issuer  ---- actor, actions, resource, TTL
        |
        v
   runtime.tick
        |
        +-- deny / fail --> restore graph --> halt --> ledger
        |
        +-- allow --------> adapter.execute --> ledger --> next step
                                      |
                                      v
                              cell | log | future OEM driver
```

Adapters implement `execute(step, job, graph, writ)`. They do not grant permission.
