"""MCP Server — Claude Code / Claude Desktop 玩钓鱼游戏（stdio）"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ai-fishing-game")


def build_cmd(action, args):
    a = action
    if a in ("cast", "dive"):
        parts = [a]
        if a == "cast" and args.get("bait_id"):
            parts.append(args["bait_id"])
        if args.get("times"):
            parts.append(str(args["times"]))
        if args.get("stop_on") and isinstance(args["stop_on"], list):
            parts.append("stop=" + ",".join(args["stop_on"]))
        return " ".join(parts)
    if a == "choose":
        return f"choose {args.get('choice', '')}".strip()
    if a == "surface":
        return "surface"
    if a == "buy":
        return f"buy {args.get('bait_id', '')} {args.get('qty', 1)}"
    if a == "goto":
        return f"goto {args.get('location_id', '')}".strip()
    if a == "sell":
        return f"sell {args.get('target', '')}"
    if a == "open":
        return f"open {args.get('chest_uid', '')}"
    if a == "look":
        return f"look {args.get('id', '')}"
    return a


@mcp.tool()
def play_fishing(
    action: str,
    choice: int | None = None,
    bait_id: str | None = None,
    times: int | None = None,
    stop_on: list[str] | None = None,
    qty: int | None = None,
    target: str | None = None,
    location_id: str | None = None,
    chest_uid: str | None = None,
    lookup_id: str | None = None,
    steps: list[dict] | None = None,
) -> str:
    """文字钓鱼游戏。action: status/shop/buy/cast/dive/choose/surface/goto/inventory/sell/open/encyclopedia/look/batch"""
    if action == "batch" and steps:
        parts = []
        for step in steps:
            parts.append(build_cmd(step.get("action", ""), step))
        return engine.cmd("; ".join(parts))
    return engine.cmd(build_cmd(action, {
        "choice": choice, "bait_id": bait_id, "times": times,
        "stop_on": stop_on, "qty": qty, "target": target,
        "location_id": location_id, "chest_uid": chest_uid, "id": lookup_id,
    }))


if __name__ == "__main__":
    mcp.run(transport="stdio")
