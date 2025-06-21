import os
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    TResponseInputItem,
    input_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper,
    InputGuardrailTripwireTriggered,
)  # type: ignore
from agents.run import RunConfig  # type: ignore
import chainlit as cl  # type: ignore
import requests  # type: ignore
from pydantic import BaseModel

load_dotenv()

gemini_api_key = os.getenv("api_key")
if not gemini_api_key:
    raise ValueError("api_key environment variable is not set.")


@function_tool
def get_crypto_price(symbol: str) -> str:
    """
    Returns the current price of the given cryptocurrency symbol from Binance.
    Example symbol: BTCUSDT, ETHUSDT
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        data = response.json()
        return f"💰 The current price of {symbol.upper()} is ${data['price']}"
    except Exception as e:
        return f"❌ Failed to fetch price: {str(e)}"


@cl.on_chat_start
async def on_chat_start():

    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
    )

    class CryptoPriceRequest(BaseModel):
        is_symbol: bool
        symbol: str
    
    input_guardrail_agent = Agent(
        name="InputGuardrailAgent",
        instructions="You only check if the user input is about crypto currency price or not.",
        output_type=CryptoPriceRequest,
        model=model
    )

    @input_guardrail    
    async def input_guardrail_function(
         ctx : RunContextWrapper[None],
        agent: Agent,
        input: TResponseInputItem
     ) -> GuardrailFunctionOutput:
    
      result = await Runner.run(
          starting_agent=input_guardrail_agent,
          context=ctx.context,
          input=input,
        )
      output = result.final_output

      return GuardrailFunctionOutput(
         output_info=output.symbol,  # tool ko symbol chahiye
         tripwire_triggered=not output.is_symbol
      ) 


    agent = Agent(
        name="CryptoDataAgent",
        instructions="You are a crypto assistant. Use tools to fetch live prices of cryptocurrencies.",
        model=model,
        tools=[get_crypto_price],
        input_guardrails=[input_guardrail_function]

    )

    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    cl.user_session.set("agent", agent)

    await cl.Message(
        content="👋 Welcome! Ask me the current rate of any cryptocurrency like BTCUSDT or ETHUSDT."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent = cl.user_session.get("agent")
    config = cl.user_session.get("config")
    chat_history = cl.user_session.get("chat_history")

    chat_history.append({"role": "user", "content": message.content})

    try:
        runner = Runner.run_sync(
            starting_agent=agent,
            input=chat_history,
            run_config=config,
        )

        response = runner.final_output
        msg.content = response
        await msg.update()

        cl.user_session.set("chat_history", runner.to_input_list())
    except InputGuardrailTripwireTriggered as e:
        print("Your question is not related to cryptocurrency. Please ask about crypto prices like BTCUSDT or ETHUSDT.", e)
        msg.content = "Your question is not related to cryptocurrency. Please ask about crypto prices like BTCUSDT or ETHUSDT."
        await msg.update()
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
