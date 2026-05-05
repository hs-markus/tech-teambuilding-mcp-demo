import json
from pathlib import Path

from fastmcp import FastMCP

SNIPPETS_DIR = Path("./snippets")

mcp = FastMCP("snippet-library")


def load_snippets() -> list[dict]:
    """Read all snippet JSON files from SNIPPETS_DIR and return them as a list."""
    snippets = []
    for path in sorted(SNIPPETS_DIR.glob("*.json")):
        try:
            snippets.append(json.loads(path.read_text()))
        except (json.JSONDecodeError, OSError):
            pass
    return snippets


@mcp.tool()
def list_snippets(language: str | None = None, tag: str | None = None) -> str:
    """List all saved code snippets, with optional filtering by language or tag.

    Use this tool when the user wants to browse or discover available snippets.
    Returns a summary of each snippet including its name, language, and description.
    Pass `language` to filter to a specific programming language (e.g. 'javascript').
    Pass `tag` to filter by a specific tag (e.g. 'highcharts').
    """
    snippets = load_snippets()

    if language:
        snippets = [s for s in snippets if s.get("language", "").lower() == language.lower()]
    if tag:
        snippets = [s for s in snippets if tag.lower() in [t.lower() for t in s.get("tags", [])]]

    if not snippets:
        return "No snippets found matching your criteria."

    lines = [f"Found {len(snippets)} snippet(s):\n"]
    for s in snippets:
        tags = ", ".join(s.get("tags", []))
        lines.append(f"- **{s['name']}** ({s.get('language', 'unknown')}): {s.get('description', '')}")
        if tags:
            lines.append(f"  Tags: {tags}")
    return "\n".join(lines)


@mcp.tool()
def get_snippet(name: str) -> str:
    """Retrieve a specific code snippet by name and return it with its full code.

    Use this tool when the user asks to see, view, or retrieve a particular snippet.
    Returns the snippet metadata and code formatted as markdown.
    `name` should be the kebab-case name of the snippet (e.g. 'highcharts-column').
    """
    path = SNIPPETS_DIR / f"{name}.json"

    if not path.exists():
        return f"Snippet '{name}' not found. Use list_snippets to see available snippets."

    snippet = json.loads(path.read_text())
    language = snippet.get("language", "")
    lines = [
        f"## {snippet['name']}",
        f"**Language:** {language}",
        f"**Description:** {snippet.get('description', '')}",
        f"**Tags:** {', '.join(snippet.get('tags', []))}",
        "",
        f"```{language}",
        snippet.get("code", ""),
        "```",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# TODO 1: Implement save_snippet
# ---------------------------------------------------------------------------
#
# Build a tool that saves a new code snippet to SNIPPETS_DIR.
#
# Decorator: @mcp.tool()
# Function signature:
#   def save_snippet(name: str, language: str, description: str,
#                    tags: list[str], code: str) -> str:
#
# What it should do:
#   - Construct the file path as SNIPPETS_DIR / f"{name}.json"
#   - Build a dict with keys: name, language, description, tags, code
#   - Write it to disk as formatted JSON (use json.dumps with indent=2)
#   - Return a confirmation string, e.g. "Snippet 'name' saved."
#
# Hint: look at get_snippet above to see how path construction and json.loads
# work — save_snippet is the mirror image of that.
#
# Don't forget a docstring! It tells the AI when to call this tool.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# TODO 2: Implement search_snippets
# ---------------------------------------------------------------------------
#
# Build a tool that searches across all snippets using a free-text query.
#
# Decorator: @mcp.tool()
# Function signature:
#   def search_snippets(query: str) -> str:
#
# What it should do:
#   - Call load_snippets() to get all snippets
#   - For each snippet, check whether `query` (case-insensitive) appears in
#     any of: name, description, code, or any item in tags
#   - Return a formatted list of matches — you can reuse the format from
#     list_snippets, or invent your own
#   - If nothing matches, return a helpful "no results" message
#
# Hint: convert both the query and each field to .lower() before comparing,
# e.g.: if query.lower() in snippet.get("code", "").lower()
#
# Don't forget a docstring!
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# TODO 3 (bonus): Add your own tool
# ---------------------------------------------------------------------------
#
# Some ideas to get you started — pick one or invent something:
#
#   - delete_snippet(name): remove a snippet file and confirm deletion
#   - list_tags(): return all unique tags across all snippets, sorted
#   - import_from_url(url, name, language, description): fetch code from a
#     URL and save it as a new snippet
#   - rename_snippet(old_name, new_name): rename a snippet file
#   - snippet_count(): return a breakdown of snippets per language
#
# ---------------------------------------------------------------------------
