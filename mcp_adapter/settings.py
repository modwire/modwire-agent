import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdapterSettings:
    api_url: str
    api_key_file: Path
    host: str = "127.0.0.1"
    port: int = 8200
    version: str = "0.1.0"

    @classmethod
    def from_environment(cls):
        return cls(
            api_url=os.environ["SCAFFOLDING_API_URL"],
            api_key_file=Path(os.environ["SCAFFOLDING_API_KEY_FILE"]),
            host=os.getenv("MCP_ADAPTER_HOST", "127.0.0.1"),
            port=int(os.getenv("MCP_ADAPTER_PORT", "8200")),
            version=os.getenv("MCP_ADAPTER_VERSION", "0.1.0"),
        )

    def api_key(self) -> str:
        key = self.api_key_file.read_text().strip()
        if not key:
            raise ValueError(f"API key file is empty: {self.api_key_file}")
        return key
