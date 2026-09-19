
# Krish naik AgenticAI 3.0 Notes

## MCP (Model context protocol)
MCP was developed by anthropic. MCP is an opensource standard for connecting AI applications to external systems. In the begining everyone had to create custom tools that can perform operations they wanted to do example to read email, write email etc. But with MCP, email provider like gmail will provide an MCP server that contains access to all tools, and other required items such as prompt and resources. This helps model to connect as a client to those MCP servers. We can this way connect to any MCP server that we need. 
MCP server is a collection of tools which we access to perform actions. 
In claudeai connectors we see are MCP servers basically provided by different companies. 

With MCP, a developer builds one MCP server for their tool (like GitHub, Google Drive, or a local database), and any AI model that supports MCP can instantly use it.

Advantages of MCP
* Easy to define and access
* scalable - any number of users can connect to mcp
* No redundant code
* Access to all tools and applications - every application will want to create mcp servers to support more user base. 
* Less prone to failure

Negatives of MCP
* complex to set up
* many servers run locally
* less idea about implementation (inside the mcp server is blackbox)

MCP is just a shared toolbox — a standard-shaped collection of tools and APIs that any AI model can reach into, instead of every developer building their own private toolbox from scratch. Tools are what you can order. Resources are the reservation book you're allowed to check. Prompts are the pre-written specials card suggesting what to order - three different kinds of help, from one restaurant.


* Claude desktop, cursor etc is the HOST that runs the MCP client. It knows MCP protocol. 
* MCP Client calls MCP Server over STDIO or Streamable HTTP option. 
* Server calls the real API
* Result flow all the way back to the client 


When the claude desktop starts up it sends initialization message to each connector it is set up to connect to. In MCP world, there is a single host used with multiple clients to connect to multiple connector. 

```mermaid
flowchart LR
    P["Person"] --> H["Host"] --> C["Client"] --> S["Server"]
```
For example, host is like mobile phone, client is like sim card, and connection to Jio needs one sim card, connection to airtel needs another sim card, but for all of them, they use same host. This is the underlying idea. So claude desktop uses single host to connect to all the connectors. This helps with decoupling individual connections , safety, parallelism and scalability in connections. 

```mermaid
flowchart TB
    Host["Host (AI Application)"] --> C1[Client 1] --> S1[(Server A)]
    Host --> C2[Client 2] --> S2[(Server B)]
    Host --> C3[Client 3] --> S3[(Server C)]
```
Transport layer: client and server speak JSON-RPC 2.0, not plain REST. Two transport types — STDIO for local servers, Streamable HTTP for remote/hosted servers

**More notes from Mayank**

<a href="https://github.com/mayank953/Live-Class-2026/blob/main/classes_summary/16%20-%2023%20Aug%20-%20MCP%20Introduction.md" target="_blank">MCP-Host-Client-Server</a>


![Host-Client-Server diagram.](images/mcp-host-client-server.png "MCP Host-Client-Server")

MCP Server contains tools, resources, prompts.

### MCP Client
HOST never connect to server directly. They use client that talks to the server. Host and Server speak the same language. 
* user ask host for send an email 
* host send this request to client
* client makes a structured request to server. They use JSON-RPC for this
* server responds with structured response
* For each MCP server, host will spin off a seperate client

This 1:1 relationship between client and server has benefits.
* scalability of clients and servers 
* security impact is minimal to individual connection
* each connection can have its own authentication mechanism
* client and server conversations can happen in parallel

### MCP Primitives

<a href="https://modelcontextprotocol.io/docs/2026-07-28/learn/server-concepts">MCP concepts documentation</a>
It explains all things a server can offer.
* **tools** - action which AI can ask server to perform (Eg: send email using gmail mcp server)
* **resources** - data sources AI can read (normally static data - Host can read this data at the begining giving host understanding of what mcp server is offering - Eg: github readme, for db server it may be schema details documentation )
* **predefined prompts** - predefined prompt template helps AI to work better

### Functions of the primitive

* MCP tools primitive has the ability to list and call tools. This helps MCP host to know what tools are available. 

| **MCP Operation** | **Purpose**              | **Returns**                            |
| ----------------- | ------------------------ | -------------------------------------- |
| **`tools/list`**  | Discover available tools | Array of tool definitions with schemas |
| **`tools/call`**  | Execute a specific tool  | Tool execution result                  |

* Resource provide static data. 

| **Method**         | **Purpose**                | **Returns**                           |
| ------------------ | -------------------------- | ------------------------------------- |
| **`resources/list`**           | List available direct resources | Array of resource descriptors          |
| **`resources/templates/list`** | Discover resource templates     | Array of resource template definitions |
| **`resources/read`**           | Retrieve resource contents      | Resource data with metadata            |
| **`subscriptions/listen`**     | Monitor resource changes        | Stream of update notifications         |

* Prompts has list and get. 

| **Method**         | **Purpose**                | **Returns**                           |
| ------------------ | -------------------------- | ------------------------------------- |
| **`prompts/list`** | Discover available prompts | Array of prompt descriptors           |
| **`prompts/get`**  | Retrieve prompt details    | Full prompt definition with arguments |


### MCP Lifecycle

* initialization \
when connection is initialized for first time 
* operation \
what operations can be performed, call tools, read resources etc
* shutdown \
where connetion is closed

**Why JSON-RPC?**
* Lightweight — plain JSON, human-readable at a glance
* Transport-agnostic — same shape over stdio or HTTP
* Two-way by design — either side can send a request
* Notifications built in — no id, fires and expects nothing back
* RPC because this allows us to call the function in a remote machine as if its a local function

MCP uses JSON-RPC 2.0 for the message format and RPC semantics, while HTTP (specifically Streamable HTTP) can be one of the transports that carries those messages.

MCP needs standardized concepts such as:

| Need                                  | JSON-RPC provides                         |
| ------------------------------------- | ----------------------------------------- |
| Request → response matching           | `id`                                      |
| Identify operation                    | `method`                                  |
| Pass arguments                        | `params`                                  |
| Standard errors                       | `error`                                   |
| Notifications                         | Messages without `id`                     |
| Bidirectional RPC-style communication | Request/response + notifications          |
| Transport independence                | Same protocol can work over stdio or HTTP |


MCP uses JSON-RPC because MCP needs a standardized, transport-independent RPC message protocol. HTTP is a transport; JSON-RPC defines how MCP requests, responses, errors, and notifications are structured. MCP can therefore run over stdio or Streamable HTTP without changing the MCP message semantics.


#### Initialization

** Structure ** 
<a href="https://mcp-lifecycle.netlify.app/">mcp lifecycle docs from mayank</a>
<a href="https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle">mcp lifecycle docs</a>

* Step 1 -
A sample request structure from client to server using json rpc 2.0
![Host-Client-Server diagram.](images/mcp-client-1.png "MCP client")

* Step 2 -
Response from server to client
![Host-Client-Server diagram.](images/mcp-server-1.png "MCP server")
The id value in response from server matches with the request from client. 
The id helps to link the response to a specific request. protocolversion has to be compatible between client and server. 

* Step 3 -
Client responds back with initialized notification. 
![Host-Client-Server diagram.](images/mcp-client-2.png "MCP client")

As client sends new request for additional calls, id value is incremeneted.
After this, they are connected for the whole session. 

| Field | Meaning |
|---|---|
| `jsonrpc` | Always `"2.0"` — identifies the JSON-RPC version |
| `id` | Identifies a request so its response/error can be matched to it |
| `method` | The operation being requested |
| `params` | Arguments supplied to the method |
| `result` | Successful response returned for a request |
| `error` | Error response returned when a request fails |


In this connection is not open, once client send request it forgets it. Server sends back another request (which is a response of request from client) to provide update. 


** Version negotiation in handshake** 

* client sends it version(latest supported)
* server sends back its version(latest supported)
* if client supports it, it moves forward, otherwise it disconnects. 


**interview question**

if you want your MCP client to work with an MCP server that was built 2 years ago, the main thing is protocol-version negotiation and backward compatibility. MCP clients ensure compatibility with older servers through protocol-version negotiation during initialization and by checking the server’s advertised capabilities.

If the server supports an older MCP version, the client uses that mutually supported version and only uses features/capabilities that the server actually supports.

**Capability negotiation in handshake** 

Capability negotiation helps to confirm what both sides can do. capabilities are added under "request" or "result" from client and server respectively. 


**In latest MCP, lifecycle is deprecated and not used**

#### Operation
During the operation phase, the client and server exchange messages according to the negotiated capabilities.
Both parties MUST:
Respect the negotiated protocol version
Only use capabilities that were successfully negotiated

**Discovery**
Discovery fires automatically the instant the handshake completes — before the user even asks a question.

In discovery tools primitive will call tools/list. The server responds back with description about the tool. After this only the actual tool call from the client side. 
![Host-Client-Server diagram.](images/mcp-client-3.png "MCP client")

**Calling**
In this phase actual tool call happens with tools/call and passing the arguments. 


#### Shutdown
"Shutdown has no goodbye message of its own. The transport closing IS the goodbye."
| Transport           | Client shutdown                                                                        | Server shutdown                                                 |
| ------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **stdio**           | Close `stdin`, wait; send `SIGTERM` if it doesn't exit; use `SIGKILL` as a last resort | Server closes its output stream and exits                       |
| **Streamable HTTP** | Close the HTTP connection                                                              | Server closes unexpectedly — client should reconnect gracefully |

**<u>Transport layer connection types</u>**

shutdown depends on the type of connection made between client and server. 

**if mcp server is running locally** \
Stdio process - client connects with server running in same machine through stdio process. Example terminal running python program where terminal is client and poython program is server they talk trhough stdio to take input and get output. If they are running on same machine just close the stdio connection is enough to shutdown. Usually in this case server is running in local machine where Host and Client exist. 
* fast connection - since both running on same system 
* secure - since both running on same system 
* simple
In STDIO, No JSON-RPC message is exchanged during shutdown at all. The entire responsibility shifts to the transport layer.

**if mcp server is running remote** \
Streamable http - client talks to server over http protocol using post request. client can close connection. The url is ending in /mcp. 
see this setup has local and remote connections. \
![MCP-Server-Type diagram.](images/mcp-server-types.png "MCP server type")

**How to create MCP Server and run it locally**

MCP servers can be created and run in local. 
```
uv init mcp-warmup
uv add fastmcp
uv run python mcp_with_primitives.py
```
mcp_with_primitives.py is below
```
# Assemble the complete, final server and write it to disk

from fastmcp import FastMCP

mcp = FastMCP("Warm-Up Server")

@mcp.tool
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to MCP."

@mcp.resource("file://server-notes")
def server_notes() -> str:
    """Read-only notes about this server, straight from a local file."""
    with open("server-notes.txt") as f:
        return f.read()

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.prompt
def structured_escalation(issue_summary: str, what_was_tried: str, customer_sentiment: str) -> str:
    """Guides the AI to log a customer escalation with every required field, in order."""
    return f"""Log this customer escalation with the following structure:
Issue Summary: {issue_summary}
What Was Already Tried: {what_was_tried}
Customer Sentiment: {customer_sentiment}
Recommended Next Action: [determine this from the details above]
"""

if __name__ == "__main__":
    mcp.run()

**accessing through inspector**
```
You can access this  through a interactive inspector UI provided by an external open-source package published by Anthropic called @modelcontextprotocol/inspector. 

```
npx -y @modelcontextprotocol/inspector uv run python mcp_with_primitives.py
opened as
http://127.0.0.1:6274/?MCP_INSPECTOR_API_TOKEN=405f2544b819e21dac9800e0047057ffeed0401e737dc923fe748b6af9185512

```

When you run npx @modelcontextprotocol/inspector, npm downloads a single, pre-bundled package from the global npm registry. Inside this package is a Vite + React + Mantine single-page web application. The Local Proxy Server: When you run the npx command, it spins up a tiny local Node.js backend proxy server on your machine (typically listening on http://localhost:6274). [1] (https://mcp.so/servers/inspector)

**using mcpjam to test your local mcpserver**

You can start up mcpjam server in your local which can provide a UI using which you can test other mcp servers like the one we set up in our local. A different port to ensure it does not compete for the same 6274 port. 
```
npx @mcpjam/inspector@latest --port 4000
```

**connect as STDIO to your local mcp server**

In this case you dont start your local mcp server example. You invoke it through MCPJAM as a subprocess. 
Now you can connect to the custom fastmcp server you created using the MCPJAM tool 
by adding the server through Add Server option. Choose STDIO for MCPJAM to start your
FASTMCP server as a seperate subprocess. You dont have to run fastmcp locally while running mcpjam. MCPJam will connect to your FASTMCP and invoke it as if its a child process or a simple python file. 

```
uv --directory <folder where python file is present> run python mcp_with_primitives.py

```

![MCP-JAM-Connect local tools diagram.](images/mcp-mcpjam-localtools.png "MCP JAM local server tools")

![MCP-JAM-Connect to local diagram.](images/mcp-mcpjam-localserver.png "MCP JAM connect STDIO to local server")

**connect as Streamable HTTP to your local mcp server**

In this case you need to start your mcp server example as HTTP process so that it has a localhost HTTP url with which it can be access.
Below command is run in the folder where your mcp server code is present. It will give you a URL like   http://127.0.0.1:8000/mcp   
```
uv run fastmcp run mcp_with_primitives.py --transport http --port 8000

```
Using the above URL you can connect from MCPJAM now. 

![MCP Streamable HTTP connected.](images/mcp-http-connected.png "MCP Streamable HTTP connected")

**mcp libraries**
**mcp library**
* from official Claude/Anthropic
* In this version using mcp library you have to write more low level code where you have to define on your own list_tools and call_tools method and define your tools in there manually. 
<a href="https://github.com/mayank953/Live-Class-2026/blob/main/Complete%20MCP/first-mcp-server/recipebox_lowlevel.py">Low level code for recipebox example</a>
```
pip install mcp
```
**fastmcp library** 
* with this library you just define your tools alone using @mcp.tool decorator. You dont define list or call tools method yourself. 
```
pip install fastmcp
```
Both options give you MCP Inspector. 
Start code in mcp inspector using below
```
CLIENT_PORT=6280 npx @modelcontextprotocol/inspector python3 mcp_with_primitives.py
```
**Adding MCPServer in Claude desktop**

To add this MCP server as a connector to claude desktop run the below comman.d
```
uv run  fastmcp install claude-desktop recipebox_fastmcp.py
```
You can see this connector when you open claude desktop. If you want to remove it, 
go to terminal and run nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
Edit the file and remove the specific server added under mcpservers file. 
CNTRL + 0 and CNTRL+X to save and exit. 



#### Integrate MCPServers with Claude

**Connectors**\
We can connect to third party MCP servers from our code using MCPClient using connectors. FastMCP has MCPClient and Langchain has MCPAdapter that is also a way to connect to MCPServer as a MCPClient. 



**local servers**\
we can use config file to add local mcpservers. 
if you installed local mcp server to claude using above command it wont show up in claude connectors. For that you have to go to developer -> manage your local mcp servers > Edit Config. This will open claude_desktop_config.json and you can add your local mcp server there. If you want recipebox to show up in connectors then you need to edit config to include path to uv (using which uv). Once below is saved into claude config, and now if we restart claude we can see the connector connecting to our local server. The files we link in developer tool, can be node or python or docker based. 

```
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

**Starting mcpserver in vscode**\
command + shift + p -> add mcp server. Give the command as uv run fastapi run recipe_box.py.   In the generated mcp.json, change uv to full path where uv is present, Change the cwd to have current directory path of python. This should help to run the VS Code. Optionally, if needed restart VSCode using Cmd + Shift + P → Developer: Reload Window


**Not all third party servers are HTTP streamable**
You can have third party servers in STDIO as well. Example gmail server can be added into claude desktop using below
https://github.com/GongRzhe/Gmail-MCP-Server

```
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    }
  }
}
```

For Tavily search it has both options. For setting up local MCP server in claude desktop, we need to run tavily search install using node js like 
```npx -y tavily-mcp@latest```.
 This downloads and starts the Tavily MCP server locally using Node.js/npm. Tavily officially documents this as the local way to run its MCP server.\
 https://github.com/tavily-ai/tavily-mcp \
Then we can add it to claude desktop client like below
```
{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "your-api-key-here",
        "DEFAULT_PARAMETERS": "{\"include_images\": true, \"max_results\": 15, \"search_depth\": \"advanced\"}"
      }
    }
  }
}
```
```mermaid
flowchart TD
    A["MCP Client<br/>Claude / VS Code / Cursor"]
    B["npx -y tavily-mcp@latest"]
    C["npx resolves/downloads<br/>tavily-mcp@latest"]
    D["Tavily MCP Server<br/>Local Process"]
    E["MCP over stdio<br/>JSON-RPC messages"]
    F["Tavily API"]
    G["Web Search / Extract / Crawl / Map"]

    A -->|"Launches"| B
    B --> C
    C --> D
    A <-->|"MCP"| E
    E --- D
    D -->|"API requests"| F
    F --> G
```

### Time Tracker Project
You create FASTAPI and FastMCP server.
```text
                    TimeTrack
                       |
                  FastAPI App
                       |
             +---------+---------+
             |                   |
          /api/...              /mcp
             |                   |
        REST API             FastMCP
             |                   |
             +---------+---------+
                       |
                  database.py
                       |
                    SQLite
```
```mcp_app = mcp.http_app(path="/").```  This creates a streamable mcp server. 


```app.mount("/mcp", mcp_app)``` puts that MCP HTTP application under: ```http://127.0.0.1:9998/mcp```

Note that  ```mcp.http_app(path="/")``` its not ```path="/mcp"```. The ```app.mount("/mcp", mcp_app)``` call below it already adds that prefix. Setting both doubles it into /mcp/mcp.



```app = FastAPI(title="TimeTrack", lifespan=mcp_app.lifespan)``` 
makes FastAPI manage the MCP application's lifecycle.

**connect from claude as STDIO**
Now if you want to connect from claude desktop to this MCP and if you use
```
{
  "command": "uv",
  "args": [
    "--directory",
    ".../timetrack/",
    "run",
    "main.py"
  ]
}
``` 
That tells Claude:"Launch main.py as a local stdio MCP server." That's the problem.
Your main.py doesn't start an MCP stdio server in the timetracker project. It merely defines a fastapi app and mcp app but does not have ```if __name__ == "__main__":```

The correct way is 
```
uv run uvicorn main:app --port 9998 --reload
```
Now you have below. And mcp is available as Streamable HTTP in http://127.0.0.1:9998/mcp
```text
Terminal
   |
   | uv run uvicorn main:app --port 9998
   v
Uvicorn
   |
   v
FastAPI application
   |
   +------------------+------------------+------------------+
   |                  |                  |                  |
   v                  v                  v                  v
  /                  /api              /static             /mcp
   |                  |                  |                  |
   v                  v                  v                  v
Website          REST API          Static Files        FastMCP
                                                            |
                                                            v
                                                        SQLite
```


The mcp.run() defaults to stdio, so you would explicitly be choosing the stdio transport there so it can be connected from claude using claude config. Your current mcp.http_app() is choosing the HTTP/Streamable HTTP approach. 

| Approach                    | Claude starts process? | Connection                 |
| --------------------------- | ---------------------- | -------------------------- |
| **stdio**                   | Yes                    | stdin/stdout               |
| **Streamable HTTP, local**  | No                     | `http://localhost:.../mcp` |
| **Remote custom connector** | No                     | Public HTTPS URL           |



**switching between mcp and regular app (if fastapi is there)**\
```uv run fastmcp run main.py```
###### Starting MCP server 'TimeTrack' with transport 'stdio'
```uv run uvicorn main:app --reload```
######  now reachable at http://127.0.0.1:8000, with the MCP endpoint at /mcp
The distinction matters: uv run fastmcp run main.py starts just the MCP server object. uv run uvicorn main:app starts the whole application — the website, the REST API, and the MCP server mounted together — because app is the FastAPI instance that has everything wired into it.


**start application and curl to mcp as streamable http**

Start mcp server and application as streamable http
```
uv run uvicorn main:app --port 9998 --reload
```

Now to check if mcp is started or not do a curl to mcp url to initialize the connection.
```
curl -i -X POST http://127.0.0.1:9998/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-11-25",
      "capabilities": {},
      "clientInfo": {
        "name": "curl-test",
        "version": "1.0"
      }
    }
  }
``` 
We got the response as below. we also got mcp-session-id. 
```
HTTP/1.1 200 OK
date: Sat, 19 Sep 2026 15:36:05 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: d1247120a6a841b482984ae261e55dce
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-11-25","capabilities":{"logging":{},"prompts":{"listChanged":true},"resources":{"subscribe":false,"listChanged":true},"tools":{"listChanged":true}},"serverInfo":{"name":"TimeTrack","version":"4.0.5"}}}
```

Next we send initialized curl command to mcp to indicate we are accepting this connection.
```
curl -i -X POST http://127.0.0.1:9998/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: d1247120a6a841b482984ae261e55dce" \
  -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
  }'
```

We recieved response as 
```
HTTP/1.1 202 Accepted
date: Sat, 19 Sep 2026 15:41:22 GMT
server: uvicorn
content-type: application/json
mcp-session-id: d1247120a6a841b482984ae261e55dce
content-length: 0

```
Next we can send reques to list/tools. 
```
curl -i -X POST http://127.0.0.1:9998/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: d1247120a6a841b482984ae261e55dce" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'
```

Response we got. 
```
HTTP/1.1 200 OK
date: Sat, 19 Sep 2026 15:42:14 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: d1247120a6a841b482984ae261e55dce
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"jsonrpc":"2.0","id":2,"result":{"tools":[{"_meta":{"fastmcp":{"tags":[]}},"description":"Log a time entry. entry_date must be YYYY-MM-DD. Shows up on the website immediately.","inputSchema":{"properties":{"employee_name":{"type":"string"},"project":{"type":"string"},"entry_date":{"type":"string"},"hours":{"type":"number"},"description":{"default":"","type":"string"}},"required":["employee_name","project","entry_date","hours"],"type":"object","additionalProperties":false},"name":"log_time","outputSchema":{"type":"object","additionalProperties":true},"title":"Log Time"},{"_meta":{"fastmcp":{"tags":[]}},"description":"Get one employee's logged entries, optionally filtered to a date range (YYYY-MM-DD).","inputSchema":{"properties":{"employee_name":{"type":"string"},"start_date":{"default":"","type":"string"},"end_date":{"default":"","type":"string"}},"required":["employee_name"],"type":"object","additionalProperties":false},"name":"get_timesheet","outputSchema":{"properties":{"result":{"items":{"additionalProperties":true,"type":"object"},"type":"array"}},"required":["result"],"type":"object","x-fastmcp-wrap-result":true},"title":"Get Timesheet"},{"_meta":{"fastmcp":{"tags":[]}},"description":"Get total hours logged against a project, broken down by employee.","inputSchema":{"properties":{"project":{"type":"string"}},"required":["project"],"type":"object","additionalProperties":false},"name":"get_project_summary","outputSchema":{"type":"object","additionalProperties":true},"title":"Get Project Summary"},{"_meta":{"fastmcp":{"tags":[]}},"description":"List every project that has at least one logged time entry.","inputSchema":{"properties":{},"type":"object","additionalProperties":false},"name":"list_projects","outputSchema":{"properties":{"result":{"items":{"type":"string"},"type":"array"}},"required":["result"],"type":"object","x-fastmcp-wrap-result":true},"title":"List Projects"}]}}
```
