import io
import unittest
from contextlib import redirect_stderr
from types import SimpleNamespace
from unittest.mock import patch

import main
from main import generate_response_from_model


class FakeAssistantMessage:
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls

    def model_dump(self, exclude_none=False):
        message = {"role": "assistant"}
        if self.content is not None or not exclude_none:
            message["content"] = self.content
        if self.tool_calls:
            message["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in self.tool_calls
            ]
        return message


class FakeClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(create=self.create)
        )
        self.requests = []

    def create(self, **request):
        self.requests.append({**request, "messages": list(request["messages"])})
        return next(self.responses)


class GenerateResponseFromModelTests(unittest.TestCase):
    def test_tool_results_are_sent_until_final_response(self):
        tool_call = SimpleNamespace(
            id="call-1",
            function=SimpleNamespace(
                name="get_file_content",
                arguments='{"file_path":"main.py"}',
            ),
        )
        first_message = FakeAssistantMessage(None, tool_calls=[tool_call])
        client = FakeClient(
            [
                SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=first_message
                        )
                    ],
                    usage=SimpleNamespace(prompt_tokens=10, completion_tokens=2),
                ),
                SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=FakeAssistantMessage("Task completed.")
                        )
                    ],
                    usage=SimpleNamespace(prompt_tokens=15, completion_tokens=4),
                ),
            ]
        )
        tool_result = {
            "role": "tool",
            "tool_call_id": "call-1",
            "content": "File contents",
        }

        with patch("main.call_function", return_value=tool_result):
            result = generate_response_from_model(client, "Read main.py")

        self.assertEqual(result, ("Task completed.", 25, 6))
        self.assertEqual(len(client.requests), 2)
        self.assertIs(client.requests[1]["messages"][-2], first_message)
        self.assertEqual(client.requests[1]["messages"][-1], tool_result)

    def test_main_reports_iteration_limit_and_returns_failure_status(self):
        stderr = io.StringIO()
        with (
            patch("sys.argv", ["main.py", "Do a task"]),
            patch("main.get_api_key", return_value="test-key"),
            patch("main.create_client", return_value=object()),
            patch(
                "main.generate_response_from_model",
                side_effect=RuntimeError(
                    "Model did not complete the task within 20 turns"
                ),
            ),
            redirect_stderr(stderr),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertIn(
            "Error: Model did not complete the task within 20 turns",
            stderr.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
