#!/usr/bin/env python3
"""Validate Agent-access schemas and their cross-field conformance vectors."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("FAIL tools/verify_agent_access_vectors.py requires jsonschema")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent


def load_vector(name: str) -> dict:
    return json.loads((ROOT / "vectors" / f"{name}.json").read_text())


def successful_delivery(payload: str, record: dict, validator: Draft202012Validator) -> bool:
    if list(validator.iter_errors(record)):
        return False
    digest = "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
    appraisal = record["appraisal"]
    return (
        digest == record["payloadDigest"]
        and digest == record["headOutputHash"]
        and record["evidenceViewId"] == appraisal["evidenceViewId"]
        and appraisal["authority"] == "LOCAL"
        and appraisal["decision"] == "ACCEPT"
    )


def closed_paths(record: dict, validator: Draft202012Validator) -> bool:
    if list(validator.iter_errors(record)):
        return False
    primary = record["appraisalBoundaryId"]
    return all(
        path["state"] == "DISABLED" or path.get("boundaryId") == primary
        for path in record["paths"]
    )


def main() -> int:
    delivery_schema = json.loads((ROOT / "schemas" / "agent-delivery.json").read_text())
    paths_schema = json.loads((ROOT / "schemas" / "agent-access-deployment.json").read_text())
    Draft202012Validator.check_schema(delivery_schema)
    Draft202012Validator.check_schema(paths_schema)
    delivery_validator = Draft202012Validator(delivery_schema)
    paths_validator = Draft202012Validator(paths_schema)

    errors: list[str] = []
    for name in [f"agent-delivery-{i:03d}" for i in range(1, 6)]:
        vector = load_vector(name)
        inp = vector["input"]
        actual = successful_delivery(inp["payloadText"], inp["credential"], delivery_validator)
        expected = vector["expect"] == "accept"
        if actual != expected:
            errors.append(f"{name}: actual {'accept' if actual else 'reject'}")

    for name in ("agent-paths-001", "agent-paths-002"):
        vector = load_vector(name)
        actual = closed_paths(vector["input"]["credential"], paths_validator)
        expected = vector["expect"] == "accept"
        if actual != expected:
            errors.append(f"{name}: actual {'accept' if actual else 'reject'}")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("OK — Agent delivery and deployment-path vectors verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
