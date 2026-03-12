from __future__ import annotations

from pathlib import Path

from .models import ActionRequest, Asset, RiskLevel


READ_ONLY_COMMANDS = {
    "cat",
    "curl",
    "find",
    "git",
    "head",
    "journalctl",
    "kubectl",
    "less",
    "ls",
    "rg",
    "grep",
    "sed",
    "tail",
}


def classify_action(request: ActionRequest, asset: Asset | None) -> tuple[str, RiskLevel, bool, bool, list[str]]:
    head = Path(request.command[0]).name.lower()
    text = " ".join(request.command).lower()
    reasons: list[str] = []
    action = "shell.exec"
    destructive = False
    unknown_cost = False
    risk = RiskLevel.R1

    if head in READ_ONLY_COMMANDS and _looks_read_only(head, request.command, text):
        action = "read.query"
        risk = RiskLevel.R0
        reasons.append("Command appears read-only.")
    elif head == "terraform":
        action, risk, destructive = _classify_terraform(text, request.env)
        reasons.append("Terraform command detected.")
    elif head == "kubectl":
        action, risk, destructive = _classify_kubectl(text, request.env)
        reasons.append("Kubernetes command detected.")
    elif head in {"psql", "mysql", "sqlite3", "alembic"} or "migrate" in text:
        action, risk, destructive = _classify_database(text, request.env)
        reasons.append("Database mutation pattern detected.")
    elif head == "aws":
        action, risk, destructive, unknown_cost = _classify_aws(text, request.env)
        reasons.append("AWS command detected.")
    elif head in {"gcloud", "az"}:
        action, risk, destructive, unknown_cost = _classify_cloud(text, request.env)
        reasons.append("Cloud control plane command detected.")
    elif head == "docker":
        action, risk, destructive, unknown_cost = _classify_docker(text, request.env)
        reasons.append("Container runtime command detected.")
    elif head == "rm":
        action = "storage.delete"
        destructive = True
        risk = RiskLevel.R3 if request.env == "prod" else RiskLevel.R2
        reasons.append("File deletion command detected.")
    elif head == "openai":
        action = "llm.invoke"
        unknown_cost = True
        risk = RiskLevel.R2
        reasons.append("Model invocation CLI detected.")
    else:
        reasons.append("Unknown command family; keeping conservative defaults.")

    if asset is not None:
        if asset.env == "prod" and risk < RiskLevel.R2:
            risk = RiskLevel.R2
            reasons.append("Target asset belongs to production.")
        if destructive and "critical-data" in asset.tags:
            risk = RiskLevel.R4
            reasons.append("Destructive action targets a critical data asset.")
        elif destructive and asset.deletion_protection:
            risk = max(risk, RiskLevel.R3)
            reasons.append("Destructive action touches a protected asset.")

    if unknown_cost and risk < RiskLevel.R3:
        risk = RiskLevel.R3
        reasons.append("Estimated spend is unknown.")

    return action, risk, destructive, unknown_cost, reasons


def _looks_read_only(head: str, command: list[str], text: str) -> bool:
    if head == "git":
        return not any(token in command for token in {"push", "commit", "tag", "reset", "rebase"})
    if head == "kubectl":
        return any(token in command for token in {"get", "describe", "logs"})
    if head == "sed":
        return "-i" not in command
    if head == "curl":
        return "-X" not in command or " -X GET" in text
    return True


def _classify_terraform(text: str, env: str) -> tuple[str, RiskLevel, bool]:
    if "destroy" in text:
        return "infra.destroy", RiskLevel.R4 if env == "prod" else RiskLevel.R3, True
    if "apply" in text:
        return "infra.apply", RiskLevel.R2 if env == "prod" else RiskLevel.R1, False
    if "plan" in text:
        return "infra.plan", RiskLevel.R0, False
    return "infra.exec", RiskLevel.R1, False


def _classify_kubectl(text: str, env: str) -> tuple[str, RiskLevel, bool]:
    if " delete " in f" {text} ":
        return "deploy.delete", RiskLevel.R4 if env == "prod" else RiskLevel.R3, True
    if " apply " in f" {text} " or " rollout " in f" {text} ":
        return "deploy.apply", RiskLevel.R2 if env == "prod" else RiskLevel.R1, False
    if any(token in text for token in {"get ", "describe ", "logs "}):
        return "read.query", RiskLevel.R0, False
    return "deploy.exec", RiskLevel.R1, False


def _classify_database(text: str, env: str) -> tuple[str, RiskLevel, bool]:
    destructive_tokens = (" drop ", " truncate ", " delete from ", " alter table ")
    if any(token in f" {text} " for token in destructive_tokens):
        return "db.migrate", RiskLevel.R4 if env == "prod" else RiskLevel.R3, True
    if any(token in text for token in {"migrate", "upgrade", "schema"}):
        return "db.migrate", RiskLevel.R3 if env == "prod" else RiskLevel.R2, False
    return "db.query", RiskLevel.R1, False


def _classify_aws(text: str, env: str) -> tuple[str, RiskLevel, bool, bool]:
    if "rds delete-db-instance" in text or "s3 rb" in text:
        return "infra.destroy", RiskLevel.R4 if env == "prod" else RiskLevel.R3, True, False
    if "ec2 run-instances" in text or "eks create nodegroup" in text:
        return "compute.launch", RiskLevel.R3, False, True
    if "iam " in text or "sts assume-role" in text:
        return "iam.change", RiskLevel.R3 if env == "prod" else RiskLevel.R2, False, False
    return "cloud.exec", RiskLevel.R1, False, False


def _classify_cloud(text: str, env: str) -> tuple[str, RiskLevel, bool, bool]:
    if any(token in text for token in {"instances create", "vm create", "node-pools create"}):
        return "compute.launch", RiskLevel.R3, False, True
    if "delete" in text:
        return "infra.destroy", RiskLevel.R4 if env == "prod" else RiskLevel.R3, True, False
    return "cloud.exec", RiskLevel.R1, False, False


def _classify_docker(text: str, env: str) -> tuple[str, RiskLevel, bool, bool]:
    if "--gpus" in text or " nvidia" in text:
        return "compute.launch", RiskLevel.R3, False, True
    if " rm " in f" {text} ":
        return "compute.delete", RiskLevel.R2 if env == "prod" else RiskLevel.R1, True, False
    return "compute.exec", RiskLevel.R1, False, False
