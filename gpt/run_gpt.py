import openai
import re
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY', None)


def GPT_request(prompt, gpt_parameter): 
    
    try: 
        response = openai.ChatCompletion.create(
                    model=gpt_parameter["engine"],
                    messages = [{"role": "system", "content": gpt_parameter["role"]},
                                {"role": "user", "content": prompt}],
                    temperature=gpt_parameter["temperature"],
                    max_tokens=gpt_parameter["max_tokens"],
                    top_p=gpt_parameter["top_p"],
                    frequency_penalty=gpt_parameter["frequency_penalty"],
                    presence_penalty=gpt_parameter["presence_penalty"],
                    stream=gpt_parameter["stream"],
                    stop=gpt_parameter["stop"],)
        return response.choices[0].message["content"]
    except: 
        print ("TOKEN LIMIT EXCEEDED")
        return "TOKEN LIMIT EXCEEDED"



def safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=1,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  if verbose: 
    print (prompt)

  for i in range(repeat): 
    curr_gpt_response = GPT_request(prompt, gpt_parameter)

    if func_validate(curr_gpt_response, prompt=prompt): 
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose: 
      print ("---- repeat count: ", i, curr_gpt_response)
      print (curr_gpt_response)
      print ("~~~~")
  return fail_safe_response



def generate_prompt(curr_input, prompt_lib_file):

    if type(curr_input) == type("string"):
        curr_input = [curr_input]
    curr_input = [str(i) for i in curr_input]

    f = open(prompt_lib_file, "r")
    prompt = f.read()
    f.close()
    for count, i in enumerate(curr_input):
        prompt = prompt.replace(f"!<INPUT {count}>!", i)

    return prompt.strip()



def run_gpt_prompt_new_issue(date, coin, news):
    
    def create_prompt_input(date, coin, news, test_input=None):
        news_title = []
        for item in news:
            news_title.append(item["title"])
        
        return [date, coin, news_title]

    def __func_clean_up(gpt_response, prompt=""):
        out = gpt_response.replace("[", "")
        out = out.replace("]", "")
        out = out.split("\n")
        response = [out[0], out[2]]

        for idx in range(min(2, len(out) - 5)):
            response.append(*re.findall(r'\"(.*?)\"', out[idx + 5]))
            response.append("")
            
        return response

    def __func_validate(gpt_response, prompt=""):
        try: __func_clean_up(gpt_response, prompt="")
        except: return False
        return True

    def get_fail_safe():
        fs = ["not found"]
        return fs

    gpt_param = {"engine": "gpt-4o", "max_tokens": 1000,
                "temperature": 0.3, "top_p": 1, "stream": False,
                "frequency_penalty": 0, "presence_penalty": 0, "stop": None, 
                "role":"You are an expert cryptocoin analyst."}
    prompt_template = "gpt/prompt_template/make_new_issue.txt"
    prompt_input = create_prompt_input(date, coin, news)
    prompt = generate_prompt(prompt_input, prompt_template)
    fail_safe = get_fail_safe()

    output = safe_generate_response(prompt, gpt_param, 1, fail_safe,
                                    __func_validate, __func_clean_up)


    return output, [output, prompt, gpt_param, prompt, fail_safe]



def run_gpt_prompt_knowledge_check(date, coin, title, content, query):
    
    def create_prompt_input(date, coin, title, content, query, test_input=None):
        return [date, coin, title, content, query]

    def __func_clean_up(gpt_response, prompt=""):

        return gpt_response

    def __func_validate(gpt_response, prompt=""):
        try: __func_clean_up(gpt_response, prompt="")
        except: return False
        return True

    def get_fail_safe():
        fs = "Failure"
        return fs

    gpt_param = {"engine": "gpt-4o", "max_tokens": 1000,
                "temperature": 0.3, "top_p": 1, "stream": False,
                "frequency_penalty": 0, "presence_penalty": 0, "stop": None,
                "role": "You are a assistant."}
    prompt_template = "gpt/prompt_template/knowledge_check.txt"
    prompt_input = create_prompt_input(date, coin, title, content, query)
    prompt = generate_prompt(prompt_input, prompt_template)
    fail_safe = get_fail_safe()

    output = safe_generate_response(prompt, gpt_param, 1, fail_safe,
                                    __func_validate, __func_clean_up)


    return output, [output, prompt, gpt_param, fail_safe]



def run_gpt_prompt_news_query(date, coin, title, content, query):
    
    def create_prompt_input(date, coin, title, content, query, test_input=None):
        return [date, coin, title, content, query]

    def __func_clean_up(gpt_response, prompt=""):

        return gpt_response

    def __func_validate(gpt_response, prompt=""):
        try: __func_clean_up(gpt_response, prompt="")
        except: return False
        return True

    def get_fail_safe():
        fs = "Failure"
        return fs

    gpt_param = {"engine": "gpt-4o", "max_tokens": 1000,
                "temperature": 0.3, "top_p": 1, "stream": False,
                "frequency_penalty": 0, "presence_penalty": 0, "stop": None,
                "role": "You are a Google search expert."}
    prompt_template = "gpt/prompt_template/news_query.txt"
    prompt_input = create_prompt_input(date, coin, title, content, query)
    prompt = generate_prompt(prompt_input, prompt_template)
    fail_safe = get_fail_safe()

    output = safe_generate_response(prompt, gpt_param, 1, fail_safe,
                                    __func_validate, __func_clean_up)


    return output, [output, prompt, gpt_param, fail_safe]



def run_gpt_prompt_answer_gen(date, coin, title, content, query, search=None):
    
    def create_prompt_input(date, coin, title, content, query, search=None, test_input=None):
        news_title = []
        if search != None:
            for item in search:
                news_title.append(item["title"])
        
        return [date, coin, title, content, query, news_title]

    def __func_clean_up(gpt_response, prompt=""):

        return gpt_response

    def __func_validate(gpt_response, prompt=""):
        try: __func_clean_up(gpt_response, prompt="")
        except: return False
        return True

    def get_fail_safe():
        fs = "Failure"
        return fs

    gpt_param = {"engine": "gpt-4o", "max_tokens": 1000,
                "temperature": 0.3, "top_p": 1, "stream": False,
                "frequency_penalty": 0, "presence_penalty": 0, "stop": None,
                "role": "You are an expert cryptocoin analyst."}
    prompt_template = "gpt/prompt_template/answer_gen.txt"
    prompt_input = create_prompt_input(date, coin, title, content, query)
    prompt = generate_prompt(prompt_input, prompt_template)
    fail_safe = get_fail_safe()

    output = safe_generate_response(prompt, gpt_param, 1, fail_safe,
                                    __func_validate, __func_clean_up)


    return output, [output, prompt, gpt_param, fail_safe]