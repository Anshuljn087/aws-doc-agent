import unittest
from unittest.mock import patch

import agent


class AgentFallbackTests(unittest.TestCase):
    def test_agent_answer_uses_local_docs_when_kb_is_unavailable(self):
        with patch.object(agent, "KB_ID", None), patch.object(agent, "retrieve", return_value=[]):
            answer = agent.agent_answer("How do I enable S3 versioning?")

        self.assertIn("versioning", answer.lower())
        self.assertIn("enable", answer.lower())

    def test_agent_answer_rewrites_follow_up_queries_with_history(self):
        history = [
            {"role": "user", "content": "Tell me about AWS Lambda"},
            {"role": "assistant", "content": "AWS Lambda is a serverless compute service."},
        ]

        with patch.object(agent, "KB_ID", "test-kb"), patch.object(agent, "generate", return_value="ok") as mock_generate, patch.object(agent, "retrieve", return_value=[{"content": {"text": "lambda"}}]) as mock_retrieve:
            agent.agent_answer("explain in easy words", history=history)

        self.assertTrue(mock_retrieve.called)
        self.assertIn("lambda", mock_retrieve.call_args.args[0].lower())
        self.assertIn("easy", mock_retrieve.call_args.args[0].lower())
        mock_generate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
