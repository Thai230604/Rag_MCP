"""Test MCP server tools"""
import subprocess
import json
import sys

def test_mcp_tools():
    """Test MCP server via stdio"""
    
    # Start MCP server process
    process = subprocess.Popen(
        ["uv", "run", "python", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # Send request
    process.stdin.write(json.dumps(init_request) + "\n")
    process.stdin.flush()
    
    # Read response
    response = process.stdout.readline()
    print("Initialize response:", response)
    
    # List tools request
    list_tools = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    process.stdin.write(json.dumps(list_tools) + "\n")
    process.stdin.flush()
    
    response = process.stdout.readline()
    print("Tools list:", response)
    
    process.terminate()

if __name__ == "__main__":
    test_mcp_tools()
