from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import GPT4All
template = "Please act as an assistant named Maya created by Takashi Tech leading company in Japan. Please provide the answer in a short way. Question: {question}" #(recommended)
prompt = PromptTemplate(template=template, input_variables=["question"])
local_path = (r"\MODELS\mistral-7b-instruct-v0.1.Q3_K_M.gguf")
llm = GPT4All(model=local_path, backend="gptj", verbose=True)
llm_chain = LLMChain(prompt=prompt, llm=llm)


# Create your views here.
@csrf_exempt
def testapi(request):
    # Important string additions for correct processing by Mistral Instruct
    str1 = "###Human:\\n"
    str2 = "\\n###Maya:"

    if request.method == "GET":
        return JsonResponse({"info":"use post method"})

    if request.method == "POST":
        question = request.POST.get('question', '')
        response = llm_chain.invoke(str1 + question + str2,return_only_outputs=True) #return type is dictionary
        json={"solution":f"{response['text']}"}
        return JsonResponse(json)