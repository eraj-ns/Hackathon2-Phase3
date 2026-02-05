"""
Test script to validate the MCP Server implementation.
"""

def test_mcp_server_imports():
    """Test that the MCP server can be imported without errors."""
    try:
        from src.mcp.server import TaskManagementMCPServer
        print("✓ Successfully imported TaskManagementMCPServer")

        # Try to instantiate the server
        server = TaskManagementMCPServer()
        print("✓ Successfully instantiated TaskManagementMCPServer")

        # Try to get the tools
        tools = server.get_tools()
        print(f"✓ Successfully retrieved tools: {[tool['name'] for tool in tools]}")

        print("\n✓ All MCP Server imports and basic functionality working correctly!")
        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_individual_tools():
    """Test that individual tools can be imported."""
    try:
        from src.mcp.tools.add_task import add_task
        from src.mcp.tools.list_tasks import list_tasks
        from src.mcp.tools.update_task import update_task
        from src.mcp.tools.complete_task import complete_task
        from src.mcp.tools.delete_task import delete_task

        print("✓ Successfully imported all individual tools")
        return True

    except ImportError as e:
        print(f"✗ Tool import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error in tool imports: {e}")
        return False


if __name__ == "__main__":
    print("Testing MCP Server Implementation...\n")

    print("1. Testing MCP Server imports:")
    server_test_passed = test_mcp_server_imports()

    print("\n2. Testing individual tool imports:")
    tools_test_passed = test_individual_tools()

    print(f"\nResults:")
    print(f"- Server test: {'PASSED' if server_test_passed else 'FAILED'}")
    print(f"- Tools test: {'PASSED' if tools_test_passed else 'FAILED'}")

    if server_test_passed and tools_test_passed:
        print("\n🎉 All tests passed! MCP Server implementation is ready.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")