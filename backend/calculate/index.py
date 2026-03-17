import json
import os
from openai import OpenAI

def handler(event: dict, context) -> dict:
    """Обрабатывает запрос к AI-калькулятору и возвращает результат расчёта."""

    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }

    body = json.loads(event.get('body', '{}'))
    question = body.get('question', '').strip()

    if not question:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Вопрос не может быть пустым'})
        }

    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': (
                    'Ты — умный калькулятор. Пользователь задаёт задачу или вопрос на любую тему: '
                    'финансы, здоровье, строительство, физика, математика, кулинария, и т.д. '
                    'Твоя задача — чётко посчитать и дать ответ. '
                    'Формат ответа: сначала краткий результат (1-2 предложения), '
                    'затем короткое объяснение как считал (2-3 предложения). '
                    'Не используй markdown. Отвечай на языке пользователя.'
                )
            },
            {'role': 'user', 'content': question}
        ],
        max_tokens=500,
        temperature=0.3
    )

    answer = response.choices[0].message.content

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'answer': answer}, ensure_ascii=False)
    }
