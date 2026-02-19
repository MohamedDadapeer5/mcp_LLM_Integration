"""Test suite for QA Bot MCP Server"""

import json
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from server import (
    KnowledgeBase,
    IntentDetector,
    ActionExecutor,
    QABotConfig,
    SearchType
)


class TestKnowledgeBase:
    """Test knowledge base search functionality"""

    def test_text_search(self):
        """Test text-based search"""
        docs = [
            {"id": "1", "title": "Account Balance", "content": "Check your account balance online"},
            {"id": "2", "title": "Transfer Money", "content": "Transfer funds between accounts"},
        ]
        kb = KnowledgeBase(docs)
        results = kb.text_search("balance", top_k=5)
        
        assert len(results) > 0
        assert results[0]["id"] == "1"

    def test_hybrid_search(self):
        """Test hybrid search"""
        docs = [
            {"id": "1", "title": "Account", "content": "balance information"},
            {"id": "2", "title": "Transfer", "content": "move money"},
        ]
        kb = KnowledgeBase(docs)
        results = kb.hybrid_search("balance", top_k=2)
        
        assert len(results) <= 2


class TestIntentDetector:
    """Test intent detection"""

    def test_detect_intent(self):
        """Test intent detection"""
        intents = [
            {
                "name": "check_balance",
                "description": "Check account balance",
                "keywords": ["balance", "check"],
                "fallback": False,
                "escalate_to_human": False
            }
        ]
        detector = IntentDetector(intents)
        intent = detector.detect("What is my balance?")
        
        assert intent is not None
        assert intent.name == "check_balance"

    def test_fallback_intent(self):
        """Test fallback intent"""
        intents = [
            {
                "name": "default",
                "description": "Default",
                "keywords": [],
                "fallback": True,
                "escalate_to_human": False
            }
        ]
        detector = IntentDetector(intents)
        intent = detector.detect("Something random")
        
        assert intent is not None
        assert intent.fallback


class TestActionExecutor:
    """Test action execution"""

    @pytest.mark.asyncio
    async def test_mock_action(self):
        """Test mock action execution"""
        actions = [
            {
                "name": "create_ticket",
                "type": "mock",
                "mock_response": {"status": "created"}
            }
        ]
        executor = ActionExecutor(actions)
        result = await executor.execute("create_ticket", {"subject": "Test"})
        
        assert result["status"] == "created"

    @pytest.mark.asyncio
    async def test_unknown_action(self):
        """Test unknown action"""
        executor = ActionExecutor([])
        result = await executor.execute("unknown", {})
        
        assert "error" in result


class TestConfig:
    """Test configuration loading"""

    def test_load_yaml_config(self, tmp_path):
        """Test YAML config loading"""
        config_content = """
industry: test
bot_persona:
  tone: friendly
knowledge:
  corpus_path: ../knowledge/test-kb.yaml
  search_type: text
intents: []
actions: []
"""
        config_file = tmp_path / "test.yaml"
        config_file.write_text(config_content)
        
        # Create dummy KB file
        kb_file = tmp_path.parent / "knowledge" / "test-kb.yaml"
        kb_file.parent.mkdir(exist_ok=True)
        kb_file.write_text("[]")
        
        config = QABotConfig(str(config_file))
        assert config.industry == "test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
