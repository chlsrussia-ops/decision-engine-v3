# decision-engine-v3

## Назначение
Manual-first decision engine третьего поколения. Генерирует рекомендации
по офферам с приоритетом ручной валидации оператором перед применением.

## Стек
- Python, FastAPI
- shared-contracts
- PostgreSQL

## Место в экосистеме
Новое поколение движка решений (manual-first подход). Полная картина:
[chlsrussia-ops/content-factory-v4 → docs/ARCHITECTURE_MAP.md](https://github.com/chlsrussia-ops/content-factory-v4/blob/main/docs/ARCHITECTURE_MAP.md)

## Запуск
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Статус
Активный (прото v3).
