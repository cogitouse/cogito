"""Entry point for Cogito."""

import argparse
import asyncio
import sys

from cogito.config.settings import load_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cogito",
        description="AI consciousness and AGI readiness evaluation",
    )
    sub = parser.add_subparsers(dest="command")

    # evaluate
    ev = sub.add_parser("evaluate", help="Run evaluation on a model")
    ev.add_argument("--model", required=True, help="Model identifier")
    ev.add_argument(
        "--dimensions", default="all", help="Comma-separated dimensions or 'all'"
    )
    ev.add_argument("--output", default="reports", help="Output directory")

    # agent
    ag = sub.add_parser("agent", help="Start autonomous agent")
    ag.add_argument("--self-sustain", action="store_true", help="Enable self-sustainability")

    # serve
    sv = sub.add_parser("serve", help="Launch API server")
    sv.add_argument("--host", default=None, help="Override host")
    sv.add_argument("--port", type=int, default=None, help="Override port")

    return parser.parse_args()


async def cmd_evaluate(args: argparse.Namespace) -> None:
    from cogito.eval.runner import EvaluationRunner

    settings = load_settings()
    runner = EvaluationRunner(settings)
    dims = None if args.dimensions == "all" else args.dimensions.split(",")
    results = await runner.run(model_id=args.model, dimensions=dims)
    runner.save_report(results, output_dir=args.output)


async def cmd_agent(args: argparse.Namespace) -> None:
    from cogito.core.agent import CogitoAgent

    settings = load_settings()
    agent = CogitoAgent(settings, self_sustain=args.self_sustain)
    await agent.run()


def cmd_serve(args: argparse.Namespace) -> None:
    from cogito.api.server import start_server

    settings = load_settings()
    host = args.host or settings.api.host
    port = args.port or settings.api.port
    start_server(settings, host=host, port=port)


def main() -> None:
    args = parse_args()
    if args.command == "evaluate":
        asyncio.run(cmd_evaluate(args))
    elif args.command == "agent":
        asyncio.run(cmd_agent(args))
    elif args.command == "serve":
        cmd_serve(args)
    else:
        print("Usage: python -m cogito {evaluate,agent,serve}")
        sys.exit(1)


if __name__ == "__main__":
    main()
