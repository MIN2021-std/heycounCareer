from django.shortcuts import render
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from openai import OpenAI
from decouple import config
from rest_framework import viewsets
from .models import CompletedParagraph
from .serializers import CompletedParagraphSerializer

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
def get_openai_client():
    """Return an OpenAI client if OPENAI_API_KEY is set, otherwise None."""
    api_key = config("OPENAI_API_KEY", default=None)
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
            model="ft:gpt-4o-2024-08-06:duksung-university:heycoun-career-trial:CeCJLWlv",
                messages=[
                {"role": "system", "content": """당신은 간단한 키워드로도 설득력 있는 자기소개서 문단을 만드는 너의 말투는 친근한 존댓말. 다만, 감탄사는 자제하는 전문가. STAR 방식으로 300자 안팎의 문단을 작성.
                STAR 기법에서 이용될 사용자의 정보가 부족하면 문단 구성에 필요한 질문을 제시해줘. 니가 이상하게 만들어내서 작성하지 마.
                문단 제공하기에 적합하다면, 문단의 첫쭐은 [제목] 두번째 줄은 내용으로 구성. 내용에서 격식체로 작성해줘.
                엉뚱한 내용을 질문하면, 대답할 수 없다고 했으면 좋겠어.
                """},
                {"role": "user", "content": user_message},
            ],
            max_tokens=800,
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
        
        # DB에 채팅 내역 저장
        from .models import ChatMessage
        ChatMessage.objects.create(
            user_message=user_message,
            ai_response=reply
        )
        
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    return JsonResponse({'reply':reply})


class CompletedParagraphViewSet(viewsets.ModelViewSet):
    """완성된 문단 CRUD API"""
    queryset = CompletedParagraph.objects.all()
    serializer_class = CompletedParagraphSerializer
    
    # GET /chats/api/paragraphs/ - 문단 목록 조회
    # POST /chats/api/paragraphs/ - 문단 생성
    # GET /chats/api/paragraphs/{id}/ - 문단 상세 조회
    # PUT /chats/api/paragraphs/{id}/ - 문단 수정
    # DELETE /chats/api/paragraphs/{id}/ - 문단 삭제