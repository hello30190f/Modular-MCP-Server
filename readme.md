# MCP Server
 This is an Modular MCP Server. Whatever you want can be added by adding scripts with following template. The scripts are searched recursively by the loader so you can place script anywhere within the `toolsPath`.

## Prepare
### install dependency
```bash
pip install -r requirements.txt
```

### write your settings at `settings.json`
```json
{
    "toolsPath": "",
    "useDefaultToolPath": true
}
```

### place your scripts and dependency (requirements.txt)
```py
from server import mcp  

@mcp.tool()
def hello_world(name: str) -> str:
    """挨拶を返します。"""
    return f"こんにちは、{name}さん！"
```

### start loader
```bash
python main.py --loadScript
```
### start server
```bash
python main.py --startServer
```



## Template
　This template shuold be located at specified toolsPath.
```py
from server import mcp  

@mcp.tool()
def hello_world(name: str) -> str:
    """挨拶を返します。"""
    return f"こんにちは、{name}さん！"
```

## Settings
```json
{
    "toolsPath": "",
    "useDefaultToolPath": true
}
```
### toolsPath
 You can specifiy where tools script are stored by absolute path.
### useDefaultToolPath
 You can make this MCP server resolve toolsPath. The default path is `./tools/` when consider the root as this MCP server (where `loader.py` is placed).

 