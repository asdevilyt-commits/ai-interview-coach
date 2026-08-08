from typing import List, Dict, Any
from backend.core.logger import logger


class KnowledgeGraphMemory:
    """
    Tier 3 — Knowledge Graph.
    Represents semantic relationships between Candidate, Skills, Projects, Weaknesses, and Target Companies.
    """
    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, label: str, properties: Dict[str, Any] = None):
        self._nodes[node_id] = {
            "id": node_id,
            "label": label,
            "properties": properties or {},
        }

    def add_edge(self, source_id: str, relation: str, target_id: str, properties: Dict[str, Any] = None):
        edge = {
            "source": source_id,
            "relation": relation,
            "target": target_id,
            "properties": properties or {},
        }
        if edge not in self._edges:
            self._edges.append(edge)
            logger.info(f"KnowledgeGraph Edge added: ({source_id}) -[{relation}]-> ({target_id})")

    def get_candidate_subgraph(self, candidate_id: str) -> Dict[str, Any]:
        related_edges = [e for e in self._edges if e["source"] == candidate_id or e["target"] == candidate_id]
        related_node_ids = {candidate_id}
        for e in related_edges:
            related_node_ids.add(e["source"])
            related_node_ids.add(e["target"])

        nodes = [self._nodes[nid] for nid in related_node_ids if nid in self._nodes]
        return {
            "candidate_id": candidate_id,
            "nodes": nodes,
            "edges": related_edges,
        }

    def sync_candidate_profile(self, candidate_id: str, profile_data: dict):
        self.add_node(candidate_id, "Candidate", {"name": profile_data.get("name", candidate_id)})
        
        target_role = profile_data.get("target_role")
        if target_role:
            role_id = f"role_{target_role.lower().replace(' ', '_')}"
            self.add_node(role_id, "TargetRole", {"name": target_role})
            self.add_edge(candidate_id, "TARGETING_ROLE", role_id)

        for company in profile_data.get("target_companies", []):
            comp_id = f"company_{company.lower().replace(' ', '_')}"
            self.add_node(comp_id, "Company", {"name": company})
            self.add_edge(candidate_id, "TARGETING_COMPANY", comp_id)

        for skill in profile_data.get("skills", []):
            s_name = skill.get("name") if isinstance(skill, dict) else str(skill)
            s_id = f"skill_{s_name.lower().replace(' ', '_')}"
            self.add_node(s_id, "Skill", {"name": s_name})
            self.add_edge(candidate_id, "KNOWS_SKILL", s_id)

        for weak in profile_data.get("weaknesses", []):
            w_id = f"weak_{weak.lower().replace(' ', '_')}"
            self.add_node(w_id, "Weakness", {"name": weak})
            self.add_edge(candidate_id, "WEAK_IN", w_id)


knowledge_graph_memory = KnowledgeGraphMemory()
