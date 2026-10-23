# DISCLAIMER

This repository is an educational prototype intended for experimentation and learning. It has not been designed, security-hardened, or tested for professional or production use, and it should not be used as part of professional development workflows or deployed in a production environment. Do not use it with sensitive data, production credentials, or systems that require dependable security, privacy, or availability. Use it only in an isolated, non-production environment and review the code before adapting it for other purposes.

## First AI-AGENT (no cool name yet)

Personal Project to learn how AI agents work. This project is being made following: [bootdev/ai-agent](https://www.boot.dev/courses/build-ai-agent-python).

### Project structure and execution flow

```text
.
├── calculator/                 # Sample project the agent can inspect and run
│   ├── main.py                 # Calculator CLI
│   ├── pkg/
│   │   ├── calculator.py       # Expression parsing and evaluation
│   │   └── render.py           # JSON result formatting
│   └── tests.py                # Calculator unit tests
├── functions/                  # Agent tools, restricted to calculator/
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
├── tests/                      # Tests for agent tools and request flow
├── call_function.py            # Tool schemas and function dispatch
├── config.py                   # Shared helper configuration
├── main.py                     # Chat CLI and model/tool loop
├── prompts.py                  # Agent system prompt
├── pyproject.toml              # Python dependencies and project metadata
├── uv.lock
└── README.md
```

The root `main.py` is the agent's command-line entry point. It sends the system
prompt and user request to the OpenRouter chat completions API using the OpenAI
Python SDK. It keeps the conversation history, executes requested tools, adds
their results to the history, and repeats until the model returns a final
response (up to 20 model turns).

`call_function.py` defines the available tool schemas and dispatches model tool
calls to the matching helpers in `functions/`. The helpers list, read, write,
or run files within the `calculator/` working directory. `prompts.py` instructs
the model how to inspect and act on that project. `config.py` holds shared
helper settings, including the maximum file-content length.

The `calculator/` directory is the sample codebase operated on by the agent.
Its CLI in `calculator/main.py` evaluates expressions using
`calculator/pkg/calculator.py` and formats results as JSON using
`calculator/pkg/render.py`.

Run the agent from the repository root with a prompt in quotes:

```sh
uv run main.py "Explain how the calculator renders the result to the console."
uv run main.py --verbose "Fix the bug in the calculator."
```

Run the calculator and its tests with:

```sh
uv run calculator/main.py "3 + 7 * 2"
uv run calculator/tests.py
```

Run the agent loop's unit tests from the repository root with:

```sh
uv run python -m unittest tests.test_main
```

The existing file-listing, file-reading, and file-execution helper checks can
also be run as modules from the repository root:

```sh
uv run python -m tests.test_get_files_info
uv run python -m tests.test_get_file_content
uv run python -m tests.test_run_python_file
```

The project uses the [OpenAI Python SDK](https://github.com/openai/openai-python)
with [OpenRouter](https://openrouter.ai/) as its API provider. Set
`OPENROUTER_API_KEY` in the environment (or in a local `.env` file) before
running the agent.
