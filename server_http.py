import json
from pathlib import Path

from fastmcp import FastMCP

SNIPPETS_DIR = Path("./snippets")

mcp = FastMCP("snippet-library", host="0.0.0.0", port=3001)


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


@mcp.tool()
def save_snippet(
    name: str,
    language: str,
    description: str,
    tags: list[str],
    code: str,
) -> str:
    """Save a new code snippet to the library.

    Use this tool when the user wants to store a piece of code for later reuse.
    `name` should be a short kebab-case identifier (e.g. 'fetch-wrapper').
    `language` should be the programming language (e.g. 'typescript', 'python').
    `tags` should be a list of relevant keywords for filtering and search.
    Overwrites any existing snippet with the same name.
    """
    SNIPPETS_DIR.mkdir(exist_ok=True)
    path = SNIPPETS_DIR / f"{name}.json"
    data = {
        "name": name,
        "language": language,
        "description": description,
        "tags": tags,
        "code": code,
    }
    path.write_text(json.dumps(data, indent=2))
    return f"Snippet '{name}' saved."


@mcp.tool()
def search_snippets(query: str) -> str:
    """Search all snippets for a free-text query.

    Use this tool when the user wants to find snippets related to a topic or keyword.
    Searches across name, description, tags, and code (case-insensitive).
    Returns a list of matching snippets with their names and descriptions.
    """
    snippets = load_snippets()
    q = query.lower()

    matches = [
        s for s in snippets
        if q in s.get("name", "").lower()
        or q in s.get("description", "").lower()
        or q in s.get("code", "").lower()
        or any(q in t.lower() for t in s.get("tags", []))
    ]

    if not matches:
        return f"No snippets found matching '{query}'."

    lines = [f"Found {len(matches)} snippet(s) matching '{query}':\n"]
    for s in matches:
        lines.append(f"- **{s['name']}** ({s.get('language', 'unknown')}): {s.get('description', '')}")
    return "\n".join(lines)
