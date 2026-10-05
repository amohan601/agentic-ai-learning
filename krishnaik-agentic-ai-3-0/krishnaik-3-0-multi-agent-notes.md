
# Krish naik AgenticAI 3.0 Notes

<a href="./Multi Agents in Langchain/">Mayank notes - Multi agents in langchain</a>

How multiple agents work together or interact between each other? 

Usecase for Multi agent - Handover a subtask to another agent without cluttering the main agent. This helps to give **context isolation** and reduce **context overloading** for the agent. The subtask may not need all the context information of main task and by keeping a seperate agent we are minimizing the context needed for the subtask to process. 

It also helps with distribution and parallelization. Different types of agent patterns. 

* subagent
* parallel agent
* chain of agents
* controller agent (router)
* reactive agent(with evaluator and feedback loop)
* heirarchical agent (main and subagents)
* planner-executor agent


**why multi agent ?**

A single agent with multiple long prompt and many tools broken down to specialized agents with specialized tools. 

**Five patterns in use**

https://docs.langchain.com/oss/python/langchain/multi-agent


| # | Notebook | Pattern | Project |
|---|---|---|---|
| 1 | `01_Subagents_Personal_Assistant.ipynb` | Subagents | A personal assistant with a calendar sub-agent and an email sub-agent |
| 2 | `02_Handoffs_Customer_Support.ipynb` | Handoffs | A customer support agent that changes behavior as it moves through a workflow |
| 3 | `03_Router_Knowledge_Base.ipynb` | Router | A knowledge base that queries GitHub, Notion, and Slack in parallel |
| 4 | `04_Skills_SQL_Assistant.ipynb` | Skills | A SQL assistant that loads database schemas on demand |

**A quick distinction: Subagents vs. Handoffs vs. Router**

These three are the ones most often confused with each other, so it's worth being precise about what separates them:

Subagents: the supervisor is itself a full agent. It decides, turn by turn, which sub-agent-as-tool to call, and can call several in sequence or in parallel. The sub-agents don't talk to the user directly.
Handoffs: there's no supervisor doing live reasoning about where to route. Instead, state (such as current_step, or which agent is "active") determines which prompt and tools are in effect right now. Agents can hand off to each other, or a single agent can reconfigure itself.
Router: a classification step (often one structured-output LLM call, not a full agent) decides, once, which specialized agents are relevant, dispatches to all of them in parallel, and a synthesis step combines their answers. There's no multi-turn orchestration.


**supervisor pattern with subagents**

The supervisor pattern is a multi-agent architecture where a central supervisor agent coordinates specialized worker agents. 
* create tools for each sugagent. create agents inside these tools for the specific task and specific prompts for those agents
* create the supervisor agents and configure these subagent tools. 
* Then you invoke the supervisor agent so that it can run through the request and identify tool call and produce interrupt to us. 
* Another variation is supervisor (orchestrator) agent calling subagent. Then subagent calling another subagent that hidden to the supervisor. 
* orchestrator and subagent maintain separate context. each subagent handoff response to specific agent that invoked it. 
     
https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant


**handoff pattern(state machine pattern)**

The state machine pattern describes workflows where an agent’s behavior changes as it moves through different states of a task. 
The state is passed into the invoke. Agent behavior such as prompt, tools and other things are modified based on a particular state value. 
A single agent's prompt and tools change based on a state field, via middleware. 

* agent is started off with a middleware 
* middleware looks at the request and looks at the configured steps and based on the request choose a step
* step defines the dynamic prompt, tools and values the agent uses that transform that agent to specialized agent for that step

It's called "handoff" because the responsibility for handling the conversation is handed off from one specialized step to another.
The slightly confusing part is that, in the LangChain example, there aren't actually multiple agent instances. 
The same agent changes its role/configuration.

https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs-customer-support

**skills**

https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant

Think of skills as small instruction packages: the SQL agent initially sees only a short description like “Sales Analytics” or “Inventory,” and when the user asks a relevant question, the agent calls a load_skill() tool to bring the detailed schema and business rules into its context. Docs by LangChain
Implementation clue: you create a SKILLS list, expose load_skill(skill_name) as a tool, and use middleware to put only the skill descriptions into the system prompt; the LLM decides when to call load_skill(), receives the full skill as a ToolMessage, and then answers using it.


```
# Pattern 3: Skills -- minimal example.
# The agent sees lightweight skill descriptions up front, and loads full content on demand.
SKILLS = {
    "refund_policy": "Full refund if cancelled 2+ hours before showtime; 50% credit within 2 hours.",
    "booking_policy": "booking after 5 pm is double the charge.",
}

@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill's full content.

    Available skills:
    - refund_policy: refund and cancellation rules
    - booking_policy: booking policy rules
    """
    print(f"skill_name, {skill_name}")
    return SKILLS.get(skill_name, f"Unknown skill: {skill_name}")

skills_agent = create_agent(
    model,
    tools=[load_skill],
    system_prompt="You are a CineBot assistant. Use load_skill when a question needs policy detail.",
)
result = skills_agent.invoke({"messages": [{"role": "user", "content": "If I cancel 3 hours before the show, do I get a refund?"}]})
print(result["messages"][-1].content)

print('------')
result = skills_agent.invoke({"messages": [{"role": "user", "content": "If I book after 6 pm, what is the booking policy? "}]})
print(result["messages"][-1].content)

```
**Router**

The router pattern is a multi-agent architecture where a routing step classifies input and directs it to specialized agents, with results synthesized into a combined response. This pattern excels when your organization’s knowledge lives across distinct verticals (separate knowledge domains that each require their own agent with specialized tools and prompts). In this pattern routern does not get back the response, instead synthesizer agent collect the response. 

https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base

**Usecases**

| Pattern | Distributed Development | Parallelization | Multi-hop | Direct User Interaction |
|---|:---:|:---:|:---:|:---:|
| **[Subagents](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **[Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)** | — | — | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **[Skills](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **[Router](https://docs.langchain.com/oss/python/langchain/multi-agent/router)** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | — | ⭐⭐⭐ |

**Performance Comparison**

Different patterns have different performance characteristics. Key metrics

* Number of LLM invocations/Model calls. More calls means more latency and higher cost
* Tokens processed - Total context window usage across all calls. More tokens means higher processing context and potential context limits.

**Buy Coffee usecase and comparison of number of LLM calls in each pattern**

https://docs.langchain.com/oss/python/langchain/multi-agent#subagents-2

Key insight: Handoffs, Skills, and Router are most efficient for single tasks (3 calls each). Subagents adds one extra call because results flow back through the main agent—this overhead provides centralized control.

Links

<a href="./Multi Agents in Langchain/">Mayank notes - Multi agents in langchain</a>

