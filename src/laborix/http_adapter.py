from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPAdapter:
    endpoint: str
    timeout: float = 10.0
    retries: int = 2

    def request_options(self) -> dict[str, object]:
        return {"endpoint": self.endpoint, "timeout": self.timeout, "retries": self.retries}
