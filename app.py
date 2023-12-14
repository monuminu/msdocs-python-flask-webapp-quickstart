import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable.config import RunnableConfig
import os
os.environ["OPENAI_API_KEY"] = "59798b794d7a4fab9e6826bf9e28cad5"

import openai
openai.api_type = "azure"
openai.api_base = "https://monuirctc1.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_kwargs= {"engine" : "gpt-4-turbo"} , streaming = True)

from util import get_skeleton_prompt_chain

@cl.on_chat_start
def start():
    chain = get_skeleton_prompt_chain(llm)
    cl.user_session.set("chain", chain)

from langchain.callbacks import StreamingStdOutCallbackHandler

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    chain = cl.user_session.get("chain")
    async for token in chain.astream({"question": message.content}, 
                                     config = RunnableConfig(callbacks = [StreamingStdOutCallbackHandler(), 
                                                                          cl.AsyncLangchainCallbackHandler()])):
        await msg.stream_token(token)