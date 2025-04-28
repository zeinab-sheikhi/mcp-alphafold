def mcp_tool(
    api_groups: List[str] = [],
    name: str | None = None,
    description: str | None = None,
):
    def decorator(fn):
        if set(api_groups) & set(args.enabled_api_groups):
            mcp.add_tool(fn, name=name, description=description)
        return fn

    return decorator

@mcp_tool(
    api_groups=["apps", "read-only"],
    description="List all the apps available for the authenticated account.",
)