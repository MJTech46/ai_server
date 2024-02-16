from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import GPT4All
template = "Please act as an assistant named Maya created by Takashi Tech leading company in Japan. Please provide the answer in a short way. Question: {question}" #(recommended)
prompt = PromptTemplate(template=template, input_variables=["question"])
local_path = (r"C:\Users\HP\Desktop\MODELS\mistral-7b-instruct-v0.1.Q3_K_M.gguf")
llm = GPT4All(model=local_path, backend="gptj", verbose=True)
llm_chain = LLMChain(prompt=prompt, llm=llm)


# Create your views here.
@csrf_exempt
def testapi(request):
    # Important string additions for correct processing by Mistral Instruct
    str1 = "###Human:\\n"
    str2 = "\\n###Maya:"

    if request.method == "GET":
        return render(request,"api/index.html")

    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get('question')
        response = llm_chain.invoke(str1 + question + str2,return_only_outputs=True) #return type is dictionary
        solu={"solution":f"{response['text']}"}
        return JsonResponse(solu)