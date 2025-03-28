from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gpt.utils import *
from gpt.run_gpt import *

class GPTIssueView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            date = request.data.get("date")
            name = request.data.get("name")
            query = date + " " + name

            google_news = search_web(query)

            out, response = run_gpt_prompt_new_issue(date, name, google_news)

            for news in google_news:
                if news['title'] == out[2]:
                    out[3] = news['link']
                if news['title'] == out[4]:
                    out[5] = news['link']
            print(out)
            response = {
                "title": out[0],
                "content": out[1],
                "news1_title": out[2],
                "news1_link": out[3],
                "news2_title": out[4],
                "news2_link": out[5],
             }

            return Response(data=response, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class GPTPromptView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get("name")
            date = request.data.get("date")
            title = request.data.get("title")
            content = request.data.get("content")
            prompt = request.data.get("prompt")
            skip = request.data.get("skip")

            check = "NO"
            news_title = []

            if skip == "none":
                check, _ = run_gpt_prompt_knowledge_check(date, name, title,
                                                          content, prompt)

            if check != "YES" and skip != "search":

                news_query, _ = run_gpt_prompt_news_query(date, name, title,
                                                          content, prompt)
                news = search_web(news_query.split("OR")[0])

                for item in news:
                    news_title.append(item["title"])

            answer, _ = run_gpt_prompt_answer_gen(date, name, title,
                                                  content, prompt, news_title)

            return Response(data={"content": answer}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)