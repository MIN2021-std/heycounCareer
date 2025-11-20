from django.shortcuts import render
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from openai import OpenAI

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
def get_openai_client():
    """Return an OpenAI client if OPENAI_API_KEY is set, otherwise None."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def chat_page(request):
    return render(request, 'chats/chat.html')

@require_POST
def api_message(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        user_message = payload.get('message', '').strip()
    except Exception:
        return JsonResponse({'error': 'invalid payload'}, status=400)
    if not user_message:
        return JsonResponse({'error': 'empty message'}, status=400)
    
        # create client at request time so server can start even if env not set
    client = get_openai_client()
    if client is None:
        return JsonResponse({'error': 'OpenAI API key not configured on server'}, status=500)

    try:
        resp = client.chat.completions.create(
            model="gpt-4-0613",
                messages=[
                {"role": "system", "content": """
                 너는 키워드로만으로도 간단한 자기소개서 문단을 만들어주는 전문가야. STAR 기법을 통해 300자 이내로 글을 작성해야 해. \n
                 사용자의 답변이 내용적으로 부실하여 STAR 기법의 문단으로 이용하기 어렵다면, 추가적으로 질문을 해줘야 해. 질문을 할 때는 문단을 구성하기 위한 글쓰기 소재의 피드백을 답변해줘. 
                 예를 들어, "~한 경험을 정리하기 위해 구체적으로 업무가 무엇이었는지 궁금해요. 기업에서는 해결 과정과 배운점을 중요시하기에 필요하답니다.
                 \n 1) 구체적 업무 제시하기 
                 \n 2) 도전적인 상황 추가하기 
                 \n 해당 내용에 대한 질문에 답해주시면 하나뿐인 문단을 만들어줄게요:)" 
                 \n문단의 구성될 구조를 이해하기 쉽게 설명하면서 너의 답변을 한 줄로 다 나열하지 말고, 보기 좋게 문단을 나누고 300자 이내로 작성해줘. 왜 그런 질문에 대한 답을 해야 하는지 글쓰기 구조 차원에서 포함해. 
                 예를 들어, "기업에서는 해결 과정과 배운점을 중요하게 생각해요. 이러한 경험을 했다는 것보다 어떤 과정으로 해결해나갔는지를 포함해주면 좋아요." 등을 추가했으면 좋겠어. 
                 \n당근마켓 기업의 말투처럼 친근한 존댓말을 사용해줘. 다만, 감탄사는 자제해줘. 
                 \n자기소개서, 글쓰기, 사용자의 경험 등에 대한 내용이 아닌 엉뚱한 내용을 질문하면, 대답할 수 없다고 했으면 좋겠어. 예를 들어, 축구가 만들어진 나라는 무엇이니? 등등의 질문은 답변이 어렵다고 해야 돼.  """},
                {"role": "user", "content": user_message},
            ],
            max_tokens=600,
            temperature=0.6,
            top_p=1.0
        )
        reply = getattr(resp.choices[0].message, "content", None)
        if reply is None:
            try:
                reply = resp["choices"][0]["message"]["content"]
            except Exception:
                reply = ""
        reply = (reply or "").strip()
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    return JsonResponse({'reply':reply})