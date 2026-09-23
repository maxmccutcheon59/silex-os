from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    id: str
    kind: str
    attrs: dict[str, Any] = field(default_factory=dict)

    def copy(self) -> Node:
        return Node(self.id, self.kind, dict(self.attrs))


class Graph:
    """Live typed state. Single source of what is true now."""

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}

    def upsert(self, node: Node) -> Node:
        existing = self.nodes.get(node.id)
        if existing is None:
            self.nodes[node.id] = node
            return node
        existing.kind = node.kind
        existing.attrs.update(node.attrs)
        return existing

    def get(self, node_id: str) -> Node | None:
        return self.nodes.get(node_id)

    def require(self, node_id: str, **expected: Any) -> Node:
        node = self.nodes.get(node_id)
        if node is None:
            raise KeyError(f"missing node {node_id}")
        for k, v in expected.items():
            if node.attrs.get(k) != v:
                raise ValueError(f"{node_id}.{k}={node.attrs.get(k)!r} != {v!r}")
        return node

    def snapshot(self) -> dict[str, Node]:
        return {nid: node.copy() for nid, node in self.nodes.items()}

    def restore(self, nodes: dict[str, Node]) -> None:
        self.nodes = {nid: node.copy() for nid, node in nodes.items()}
