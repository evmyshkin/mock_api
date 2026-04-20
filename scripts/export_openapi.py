from __future__ import annotations

import argparse
import json
import logging

from pathlib import Path

from app.main import fastapi_app

LOGGER = logging.getLogger(__name__)


def dump_openapi(output_path: Path) -> str:
    """Generate OpenAPI JSON payload and write it to ``output_path``."""
    schema = fastapi_app.openapi()
    payload = json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding='utf-8')
    return payload


def main() -> int:
    """Export or verify the committed OpenAPI snapshot."""
    parser = argparse.ArgumentParser(description='Export FastAPI OpenAPI schema to JSON file.')
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('docs/openapi/openapi.v1.json'),
        help='Output path for exported OpenAPI JSON.',
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Fail if existing file content differs from the generated schema.',
    )

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    generated = json.dumps(fastapi_app.openapi(), ensure_ascii=False, indent=2, sort_keys=True) + '\n'

    if args.verify:
        if not args.output.exists():
            LOGGER.error('[openapi] Missing expected file: %s', args.output)
            return 1

        existing = args.output.read_text(encoding='utf-8')
        if existing != generated:
            LOGGER.error(
                '[openapi] Outdated schema at %s. Regenerate with: uv run python scripts/export_openapi.py --output %s',
                args.output,
                args.output,
            )
            return 1

        LOGGER.info('[openapi] Verified: %s', args.output)
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(generated, encoding='utf-8')
    LOGGER.info('[openapi] Exported to %s', args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
