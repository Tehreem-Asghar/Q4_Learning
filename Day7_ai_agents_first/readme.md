## OpenAI Agents SDK — Beginner-Friendly Guide with Q&A

# What Are OpenAI, Agents, and SDK?

- **OpenAI**: A company that creates AI, including advanced language models like GPT.

- **Agent**: An AI program that performs specific tasks independently.

- **SDK (Software Development Kit)** : A collection of tools and libraries that help developers build AI agents.

**Example:**
An agent works like a personal assistant — it can manage your emails, give you reminders, or automate your tasks.



# Core Concepts

- **Agents**: AI helpers that perform tasks.

- **Handoffs**: When one agent passes its task to another agent.

- **Guardrails**: Safety measures that prevent agents from doing something wrong.

- **Tracing & Observability**: Monitoring every step of an agent’s actions.



## Question / Answer


# **Q1** : The Agent class has been defined as a dataclass why?

- @dataclass is a feature in Python that automatically creates boilerplate code for a class, such as __init__(), __repr__(), and __eq__().

- The benefit is that you don’t have to write the __init__() function manually. It makes your code shorter, cleaner, and more readable — especially when the class is only used to hold data like name, tools, instructions, etc.

- In a normal class, you have to write all of this manually: 👇

```
class Agent:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    def __str__(self):
        return f"Agent(name={self.name}, instructions={self.instructions})"

    def __repr__(self):
        return f"Agent(name={self.name!r}, instructions={self.instructions!r})"
```

👆 All of this happens automatically if you use @dataclass:

```
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    instructions: str

```

- __init__, __str__, and __repr__ are automatically generated.

- The code becomes short, clean, and easy to read.

# **Conclusion:**

- With @dataclass, there’s no need to write boilerplate code — it’s the best solution for clean and fast development, especially when a class is only used to hold data.


## **Q2 A** :The system prompt is contained in the Agent class as instructions? Why you can also set it as callable?
 
- System prompt or instructions are the guidance that tells the agent how to work — like assigning a role to the agent (e.g., “You are a helpful assistant.”).

- Usually, these instructions are a fixed string that defines the agent.

- But in some cases, you need the instructions to be dynamic (changing), meaning the agent should receive different or updated instructions each time.

- That’s why the SDK is designed so you can also set instructions as a callable (function).

- When instructions are callable, each time the agent runs, the function is called and returns the latest or context-specific instructions.

**Example**
```
def dynamic_instructions():
    import datetime
    today = datetime.date.today()
    return f"You are an assistant. Today's date is {today}."

agent = Agent(
    name="DateAwareAgent",
    instructions=dynamic_instructions  # callable instead of fixed string
)

```

- **Fixed string instructions** are used when the role or behavior is constant.

- **Callable instructions** are used when the instructions need to change based on the context.



## Q2 b. But the user prompt is passed as a parameter in the run method of Runner, and the method is a classmethod — Why?

- User prompt is the input or question that you give to the agent to process at runtime. It changes every time the agent is used, depending on what the user wants.

- In contrast to system instructions (which define the agent’s role and behavior), user prompts are dynamic inputs—you don’t know them beforehand.

- That’s why, instead of storing the user prompt inside the agent itself, the SDK passes the user prompt as a parameter to the run method of the Runner class.

- The run method is a classmethod because:

- It can be called on the class itself without creating an instance.

- It manages the execution of the agent’s workflow — taking the user prompt, running the agent’s logic, handling tools, and returning results.

- This design helps keep the agent class simple (mainly instructions and tools), while the Runner handles the dynamic running and orchestration.


```
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    instructions: str  # System prompt, fixed per agent

class Runner:
    @classmethod
    def run(cls, agent: Agent, user_prompt: str):
        # Combine system prompt (instructions) with user prompt
        full_prompt = f"System: {agent.instructions}\nUser: {user_prompt}"
        print(f"Running agent '{agent.name}' with prompt:\n{full_prompt}")

# Create an agent with fixed system prompt
my_agent = Agent(name="HelperBot", instructions="You are helpful and polite.")

# Run the agent with different user prompts
Runner.run(my_agent, "What's the capital of France?")
Runner.run(my_agent, "How do I bake a cake?")

```

## **Q3** What is the purpose of the Runner class?


- The Runner class runs the agent, combines instructions and user prompt, handles tools (if any), and returns the output.

# 🧠 It manages:

- Taking user input

- Running the agent

- Returning response

- Handling logs/tracing

```
class Runner:
    @classmethod
    def run(cls, agent: Agent, user_prompt: str):
        return f"{agent.instructions} | User: {user_prompt}"
```


## Q4 What are generics in Python? Why we use it for TContext?

- Generics let us define flexible and type-safe classes.

- TContext is a generic type — it allows the Agent class to work with any kind of context.

#  Why Use Generics?

✅ **Type Safety**: Prevents errors with wrong data types.

🔁 **Reusability**: Same agent structure can handle different data.

💡 **IDE Support**: Better auto-complete and hints.

```
from dataclasses import dataclass
from typing import TypeVar, Generic

TContext = TypeVar("TContext")

@dataclass
class Agent(Generic[TContext]):
    name: str
    instructions: str
    context: TContext


```