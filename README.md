# MCP Workshop: Build a Snippet Library Server

This is a hands-on workshop for learning how to build an MCP (Model Context Protocol) server using Python and FastMCP. You will build a working snippet library — a small server that stores and retrieves code snippets — and connect it to Claude Code or Codex CLI so your AI assistant can read and write your personal code collection.

By the end you will have a server running locally over stdio and remotely over HTTP inside a Podman container.

---

## Prerequisites

- Python 3.10 or newer
- pip
- [Podman](https://podman.io/docs/installation) (for Step 4 — the container part)
- Claude Code or Codex CLI (see Step 3 / Codex section below)

---

## Quick start

```bash
git clone <this-repo>
cd mcp-workshop
pip install fastmcp
fastmcp run server.py
```

If it starts without errors, you are ready. Press Ctrl-C to stop it.

---

## Workshop steps

### Step 1 — Read the existing code

Open `server.py`. Two tools are already implemented:

- **list_snippets** — returns all snippets, optionally filtered by language or tag
- **get_snippet** — returns a single snippet by name, formatted as markdown

Read through both implementations. Notice how the `@mcp.tool()` decorator registers
each function, and how the docstring is what the AI reads to decide when to call the tool.

The `load_snippets()` helper at the top is a pattern you will reuse in your implementations.

---

### Step 2 — Fill in the TODOs

There are two required TODOs and one bonus:

**TODO 1: `save_snippet`**

Add a tool that accepts `name`, `language`, `description`, `tags`, and `code`, then
writes a JSON file to `SNIPPETS_DIR`. The comment block in `server.py` gives you the
full signature and a hint. If you get stuck, check `SOLUTIONS.md`.

**TODO 2: `search_snippets`**

Add a tool that accepts a `query` string and searches across all snippet fields
(name, description, tags, code) using case-insensitive matching. Return a list of
matches. The comment block gives you a hint about lowercasing.

**TODO 3 (bonus): Add your own tool**

See the bonus comment block in `server.py` for ideas. `SOLUTIONS.md` has three
worked examples: `delete_snippet`, `list_tags`, and `import_from_url`.

After filling in each TODO, restart with `fastmcp run server.py` to make sure it
still starts cleanly.

---

### Step 3 — Connect to Claude Code

Register your local server as an MCP server:

```bash
claude mcp add snippet-library -- fastmcp run server.py
```

Start a new Claude Code session and try these prompts:

- "List my snippets"
- "Show me the highcharts-column snippet"
- "Save a new snippet called fetch-wrapper for TypeScript — it should be an async fetch helper with error handling"
- "Search my snippets for pie chart examples"

Each prompt should trigger the corresponding tool. You can watch the tool calls in
the Claude Code output to verify things are wiring up correctly.

---

### Step 4 — Run in a Podman container (HTTP transport)

`server_http.py` is a complete version of the server (all tools implemented) that
runs over HTTP on port 3001. Build and start it with Podman:

```bash
podman build -t snippet-mcp .
podman run -p 3001:3001 snippet-mcp
```

Then register it as a remote MCP server in Claude Code:

```bash
claude mcp add snippet-remote --transport http http://localhost:3001/mcp
```

Test with the same prompts as Step 3. This time the calls go over HTTP to your
container instead of launching a local process.

Note: the container starts with only the three built-in snippets. Snippets saved
through the remote server live inside the container and will be lost when the
container stops. For persistence you would mount a volume — that is outside the
scope of this workshop, but worth exploring.

---

### Step 5 — Tackle TODO 3

Come back to `server.py` and implement the bonus tool. Once it works locally,
add it to `server_http.py` too and rebuild the container.

---

## Codex users

The same server works with Codex CLI. The MCP configuration format is slightly
different — see the [Codex MCP docs](https://developers.openai.com/codex/mcp) for
the exact config structure. The server itself requires no changes.

---

## Useful links

- [MCP specification](https://modelcontextprotocol.io)
- [Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Codex MCP docs](https://developers.openai.com/codex/mcp)
- [FastMCP repo](https://github.com/prefecthq/fastmcp)
- [Podman installation](https://podman.io/docs/installation)
