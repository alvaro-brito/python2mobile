"""
Configuration management for P2M projects
"""

import os
import toml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class ProjectConfig:
    """Project configuration"""
    name: str
    version: str
    entry: str
    
    
@dataclass
class BuildConfig:
    """Build configuration"""
    target: list
    generator: str
    llm_provider: str
    llm_model: str
    output_dir: str
    cache: bool


@dataclass
class DevServerConfig:
    """DevServer configuration"""
    port: int
    hot_reload: bool
    mobile_frame: bool


@dataclass
class StyleConfig:
    """Style configuration"""
    system: str


@dataclass
class LLMConfig:
    """LLM provider configuration"""
    provider: str
    api_key: Optional[str] = None
    model: Optional[str] = None
    base_url: Optional[str] = None
    x_api_key: Optional[str] = None


class Config:
    """Main configuration handler"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or "p2m.toml")
        self.config_data: Dict[str, Any] = {}
        self.project: Optional[ProjectConfig] = None
        self.build: Optional[BuildConfig] = None
        self.devserver: Optional[DevServerConfig] = None
        self.style: Optional[StyleConfig] = None
        self.llm: Optional[LLMConfig] = None
        
        if self.config_path.exists():
            self.load()
        else:
            self._set_defaults()
    
    def load(self) -> None:
        """Load configuration from TOML file"""
        try:
            self.config_data = toml.load(str(self.config_path))
            self._parse_config()
        except Exception as e:
            raise RuntimeError(f"Failed to load config from {self.config_path}: {e}")
    
    def _parse_config(self) -> None:
        """Parse configuration data into dataclass objects"""
        # Project config
        project_data = self.config_data.get("project", {})
        self.project = ProjectConfig(
            name=project_data.get("name", "MyApp"),
            version=project_data.get("version", "0.1.0"),
            entry=project_data.get("entry", "main.py"),
        )
        
        # Build config
        build_data = self.config_data.get("build", {})
        self.build = BuildConfig(
            target=build_data.get("target", ["android", "ios"]),
            generator=build_data.get("generator", "flutter"),
            llm_provider=build_data.get("llm_provider", "openai"),
            llm_model=build_data.get("llm_model", "gpt-4o"),
            output_dir=build_data.get("output_dir", "./build"),
            cache=build_data.get("cache", True),
        )
        
        # DevServer config
        devserver_data = self.config_data.get("devserver", {})
        self.devserver = DevServerConfig(
            port=devserver_data.get("port", 3000),
            hot_reload=devserver_data.get("hot_reload", True),
            mobile_frame=devserver_data.get("mobile_frame", True),
        )
        
        # Style config
        style_data = self.config_data.get("style", {})
        self.style = StyleConfig(
            system=style_data.get("system", "tailwind"),
        )
        
        # LLM config
        llm_data = self.config_data.get("llm", {})
        provider_data = llm_data.get(self.build.llm_provider, {})
        
        # Resolve API key: p2m.toml [llm.<provider>] → P2M_<PROVIDER>_API_KEY → standard key env vars
        _provider_upper = self.build.llm_provider.upper()
        _standard_keys = {
            "ANTHROPIC": os.getenv("ANTHROPIC_API_KEY"),
            "OPENAI": os.getenv("OPENAI_API_KEY"),
        }
        _resolved_key = (
            provider_data.get("api_key")
            or os.getenv(f"P2M_{_provider_upper}_API_KEY")
            or _standard_keys.get(_provider_upper)
        )

        self.llm = LLMConfig(
            provider=self.build.llm_provider,
            api_key=_resolved_key,
            model=provider_data.get("model") or self.build.llm_model,
            base_url=provider_data.get("base_url"),
            x_api_key=provider_data.get("x_api_key"),
        )
    
    def _set_defaults(self) -> None:
        """Set default configuration"""
        self.project = ProjectConfig(
            name="MyApp",
            version="0.1.0",
            entry="main.py",
        )
        
        self.build = BuildConfig(
            target=["android", "ios"],
            generator="flutter",
            llm_provider="openai",
            llm_model="gpt-4o",
            output_dir="./build",
            cache=True,
        )
        
        self.devserver = DevServerConfig(
            port=3000,
            hot_reload=True,
            mobile_frame=True,
        )
        
        self.style = StyleConfig(
            system="tailwind",
        )
        
        self.llm = LLMConfig(
            provider="openai",
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o",
        )
    
    def save(self, path: Optional[str] = None) -> None:
        """Save configuration to TOML file"""
        output_path = Path(path or self.config_path)
        
        config_dict = {
            "project": {
                "name": self.project.name,
                "version": self.project.version,
                "entry": self.project.entry,
            },
            "build": {
                "target": self.build.target,
                "generator": self.build.generator,
                "llm_provider": self.build.llm_provider,
                "llm_model": self.build.llm_model,
                "output_dir": self.build.output_dir,
                "cache": self.build.cache,
            },
            "devserver": {
                "port": self.devserver.port,
                "hot_reload": self.devserver.hot_reload,
                "mobile_frame": self.devserver.mobile_frame,
            },
            "style": {
                "system": self.style.system,
            },
        }
        
        with open(output_path, "w") as f:
            toml.dump(config_dict, f)
    
    def get_llm_config(self) -> LLMConfig:
        """Get LLM configuration"""
        return self.llm
