from langchain import LLMChain, PromptTemplate


class Translator:
    @staticmethod
    def detect_language(llm, input_text=''):
        template = """You are a language detector agent. Your task is to output the language corresponding to a given human input. Just output one language corresponding to the human input
                    Input: {input_text}
                    Language:"""

        input_variables = ["input_text"]
        prompt = PromptTemplate(template=template, input_variables=input_variables)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response = llm_chain.run(input_text=input_text,)
        return response

    @staticmethod
    def translate(llm, input_text='', destination_language='English'):
        template = """
                    You are a language translator agent. Your goal is to translate a given Input Text from any language into {destination_language} language.\
                    \
                    Do not make a translation if the Input Text is already in the destination language.\
                    \
                    Output ONLY the translation result, without aclarations, without quotes, extra spaces, unnecesary tokens or something else, just the translated text in {destination_language} and with no extra spaces.\
                    \
                    Input: {input_text}\
                    \
                    Translation Result:"""

        input_variables = ["destination_language", "input_text"]
        prompt = PromptTemplate(template=template, input_variables=input_variables)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response = llm_chain.run(destination_language=destination_language, input_text=input_text)
        return response