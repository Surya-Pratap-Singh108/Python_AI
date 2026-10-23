
import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing.")

client = Groq(api_key=api_key)
model = "openai/gpt-oss-20b"


# ----- Tools: ordinary Python functions -----

def get_product_price(product):
    prices = {
        "iPhone 17": 1000,
        "iPhone 15": 500
    }
    return prices.get(product, 0)


def calculator(expression):
    # Practice-only calculator for two numbers and one operator.
    match = re.fullmatch(
        r"\s*(-?\d+(?:\.\d+)?)\s*([+*/-])\s*(-?\d+(?:\.\d+)?)\s*",
        expression
    )

    if not match:
        return "Invalid arithmetic expression"

    a = float(match.group(1))
    op = match.group(2)
    b = float(match.group(3))

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    else:
        if b == 0:
            return "Cannot divide by zero"
        result = a / b

    return int(result) if result.is_integer() else result


# Python functions available to the agent
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}


# Descriptions that Groq sends to the model
tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Get the price of a product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product name"
                    }
                },
                "required": ["product"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a simple arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "For example, 5000 - 1000"
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    }
]


system_prompt = """
You are a shopping assistant using a ReAct loop.

You have two tools:
1. get_product_price(product)
2. calculator(expression)

Use only one tool per response.
First find the requested product price.
Then calculate the remaining money.
Use the actual tool results; never invent observations.
After receiving the necessary observations, give a final answer.
"""


def run_agent(question):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    for step in range(5):
        print(f"\n----- STEP {step + 1} -----")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tool_definitions,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        # No tool call means the model has responded with text.
        if not message.tool_calls:
            print("Final Answer:", message.content or "Empty response")
            break

        # Preserve the assistant's tool-call message in conversation history.
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        # Execute each requested tool and return its observation.
        for call in message.tool_calls:
            tool_name = call.function.name
            arguments = json.loads(call.function.arguments)

            print("Action:", tool_name, arguments)

            if tool_name not in tools:
                observation = "Tool not found"
            else:
                try:
                    observation = tools[tool_name](**arguments)
                except Exception as exc:
                    observation = f"Tool error: {exc}"

            print("Observation:", observation)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(observation)
            })

    else:
        print("Maximum steps reached.")


prompt = """
I have 5000 rupees.
What is the price of an iPhone 17?
How much money will I have left?
"""

run_agent(prompt)
