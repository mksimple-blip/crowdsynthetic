import datetime


def _ts() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def info(msg: str) -> None:
    print(f"[INFO] [{_ts()}] {msg}")


def warn(msg: str) -> None:
    print(f"[WARN] [{_ts()}] {msg}")


def error(msg: str) -> None:
    print(f"[ERROR] [{_ts()}] {msg}")
