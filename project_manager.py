import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from project_schema import ProjectRecord, UploadedDocument

class ProjectManager:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.projects_dir = self.base_dir / "data" / "projects"
        self.outputs_dir = self.base_dir / "outputs"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    def _project_dir(self, project_id: str) -> Path:
        return self.projects_dir / project_id

    def _project_json(self, project_id: str) -> Path:
        return self._project_dir(project_id) / "project.json"

    def _save(self, project: ProjectRecord) -> ProjectRecord:
        project.updated_at = datetime.utcnow().isoformat()
        pdir = self._project_dir(project.project_id)
        pdir.mkdir(parents=True, exist_ok=True)
        self._project_json(project.project_id).write_text(project.model_dump_json(indent=2), encoding="utf-8")
        return project

    def create_project(self, license_key: str, name: str, company_name: str, sector: str="General", currency: str="EUR", deal_type: str="M&A") -> ProjectRecord:
        project = ProjectRecord(
            project_id=str(uuid.uuid4()),
            name=name or company_name or "New Project",
            company_name=company_name or name or "Target Company",
            sector=sector or "General",
            currency=currency or "EUR",
            deal_type=deal_type or "M&A",
            license_key=license_key
        )
        return self._save(project)

    def list_projects(self, license_key: str) -> List[ProjectRecord]:
        projects = []
        for pj in self.projects_dir.glob("*/project.json"):
            try:
                p = ProjectRecord.model_validate_json(pj.read_text(encoding="utf-8"))
                if p.license_key == license_key:
                    projects.append(p)
            except Exception:
                pass
        return sorted(projects, key=lambda p: p.updated_at, reverse=True)

    def get_project(self, project_id: str, license_key: Optional[str]=None) -> ProjectRecord:
        path = self._project_json(project_id)
        if not path.exists():
            raise FileNotFoundError(project_id)
        p = ProjectRecord.model_validate_json(path.read_text(encoding="utf-8"))
        if license_key and p.license_key != license_key:
            raise PermissionError(project_id)
        return p

    def update_project(self, project_id: str, license_key: str, updates: Dict[str, Any]) -> ProjectRecord:
        p = self.get_project(project_id, license_key)
        for k, v in updates.items():
            if hasattr(p, k):
                setattr(p, k, v)
        return self._save(p)

    def set_intake(self, project_id: str, license_key: str, intake: Dict[str, Any]) -> ProjectRecord:
        p = self.get_project(project_id, license_key)
        p.intake = intake or {}
        p.module_status["bp"] = "Configured"
        return self._save(p)

    def set_financials(self, project_id: str, license_key: str, financials: Dict[str, Any]) -> ProjectRecord:
        p = self.get_project(project_id, license_key)
        p.extracted_financials = financials
        return self._save(p)

    def add_document(self, project_id: str, license_key: str, filename: str, content: bytes, category: str="financials") -> UploadedDocument:
        p = self.get_project(project_id, license_key)
        file_id = str(uuid.uuid4())
        safe = filename.replace("/", "_").replace("\\", "_")
        ddir = self._project_dir(project_id) / "documents"
        ddir.mkdir(parents=True, exist_ok=True)
        path = ddir / f"{file_id}_{safe}"
        path.write_bytes(content)
        doc = UploadedDocument(file_id=file_id, filename=safe, path=str(path), category=category)
        p.documents.append(doc)
        self._save(p)
        return doc

    def add_output(self, project_id: str, license_key: str, output_type: str, file_path: str) -> ProjectRecord:
        p = self.get_project(project_id, license_key)
        p.outputs[output_type] = file_path
        if output_type == "bp_model":
            p.module_status["bp"] = "Generated"
        elif output_type == "im_deck":
            p.module_status["deck"] = "Generated"
        elif output_type == "qoe_pack":
            p.module_status["qoe"] = "Generated"
        elif output_type == "restructuring_pack":
            p.module_status["restructuring"] = "Generated"
        return self._save(p)

    def get_output_path(self, project_id: str, license_key: str, output_type: str):
        p = self.get_project(project_id, license_key)
        path = p.outputs.get(output_type)
        if not path:
            return None
        path = Path(path)
        return path if path.exists() else None
