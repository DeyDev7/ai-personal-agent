# DISCLAIMER

This repository is an educational prototype intended for experimentation and learning. It has not been designed, security-hardened, or tested for professional or production use, and it should not be used as part of professional development workflows or deployed in a production environment. Do not use it with sensitive data, production credentials, or systems that require dependable security, privacy, or availability. Use it only in an isolated, non-production environment and review the code before adapting it for other purposes.

## First AI-AGENT (no cool name yet)

Personal Project to learn how AI agents work. This project is being made following: [bootdev/ai-agent](https://www.boot.dev/courses/build-ai-agent-python).

### Current architecture of the project

```text
root/
├── .python-version
├── calculator/
│   ├── main.py
│   ├── tests.py
│   ├── lorem.txt
│   └── pkg/
│       ├── calculator.py
│       ├── morelorem.txt
│       └── render.py
├── config.py
├── functions/
│   ├── get_file_content.py
│   ├── get_files_info.py
│   └── write_to_files.py
├── main.py
├── pyproject.toml
├── README.md
├── test_get_file_content.py
├── test_get_files_info.py
├── test_write_file.py
└── uv.lock
```

The root `main.py` provides the command-line chat client and calls the OpenRouter
chat completions API through the OpenAI SDK. The `functions/` modules provide
separate helpers to read a file, list directory entries, and write a file
within a permitted working directory. `config.py` contains shared settings,
including the maximum file-content length used by the file-reading helper.
The `test_*.py` scripts exercise those file helpers; they are currently kept
separate from the chat client's request flow.

### Tools

Project's been built using:

- [OpenAI SDK Toolkit](https://github.com/openai/openai-agents-python)
- [OpenRouter free API KEY](https://openrouter.ai/)
