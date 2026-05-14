# 🛠️ Model Context Protocol (MCP) Project Commands

#### 🏷️ _Created by hourToLearn_

This file outlines the necessary commands for setting up the project, running the MCP Inspector, registering MCP tools with the Claude CLI, and configuring them in your `settings.json` for Claude Code.

---

## 1. Project Setup (uv + Python)

These steps use `uv` for dependency management and environment setup.

### 📝 Initialize Project

Initializes a `uv` project with a specified Python version. Activate virtual environment. Add fastmcp library.

```
uv init --python 3.13

uv venv

.\.venv\Scripts\Activate.ps1

uv add fastmcp
```

## 2. Running MCP Inspector

Use the @modelcontextprotocol/inspector package to launch the Inspector for debugging and testing your tools.

🔍 Launch Inspector

```
npx @modelcontextprotocol/inspector
```

## 3. Add MCP Tools to Claude CLI

Register your custom MCP tools with the Claude Command Line Interface (CLI).

⚙️ General Format

```
claude mcp add {NAME} {COMMAND} [ARGUMENTS]
```

{NAME}: A unique, human-readable identifier for your tool (e.g., myDemoMcp).

{COMMAND}: The executable command to run the tool (e.g., uv).

[ARGUMENTS]: Any necessary arguments for the command.

💡 Example: Register your demo MCP tool
This example registers a tool named myDemoMcp that is run using uv run on a specific Python file.

```
claude mcp add myDemoMcp uv run C:\Users\user\WorkSpace\hourTolearn\main.py
```

## 4. Claude Code MCP Configuration (settings.json)

Configure your MCP servers in the settings.json file for use within the Claude Code environment.

🖥️ Example Configuration for Two MCP Tools
The following JSON block shows how to configure two tools: playwright (using npx) and a custom tool myDemoMcp (using uv.exe). This should be placed inside your main settings.json file.

```JSON
"mcpServers": {
  "playwright": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "@playwright/mcp@latest"
    ],
    "env": {}
  },
  "myDemoMcp": {
    "type": "stdio",
    "command": "C:/Users/user/.local/bin/uv.exe",
    "args": [
      "--directory",
      "C:\\Users\\user\\WorkSpace\\hourTolearnMcp\\",
      "run",
      "main.py"
    ],
    "env": {}
  }
}
```
