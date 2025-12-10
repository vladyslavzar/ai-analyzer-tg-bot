"""LLM utilities for text analysis using OpenAI-compatible API."""

import json
from typing import Any

import httpx

from app.config import settings


async def analyze_text(text: str) -> dict[str, Any]:
    """
    Analyze long text message: generate summary, extract tasks, analyze sentiment.

    Args:
        text: The text message to analyze

    Returns:
        Dictionary with:
        - summary: Concise AI summary
        - tasks: List of extracted tasks/to-dos
        - sentiment: positive/neutral/negative
    """
    if not settings.llm_api_key:
        return {
            "summary": "LLM API key not configured",
            "tasks": [],
            "sentiment": "neutral",
        }

    # Prepare the prompt
    prompt = f"""Analyze the following text message and provide:
1. A concise summary (2-3 sentences)
2. A list of tasks/to-dos mentioned (if any)
3. The sentiment (positive, neutral, or negative)

Text: {text}

Respond in JSON format:
{{
    "summary": "concise summary here",
    "tasks": ["task1", "task2"],
    "sentiment": "positive|neutral|negative"
}}"""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.llm_api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.llm_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.llm_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that analyzes text messages. Always respond with valid JSON only.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            result = response.json()

            # Extract the response content
            content = result["choices"][0]["message"]["content"].strip()

            # Try to parse JSON from the response
            # Sometimes LLM wraps JSON in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            analysis = json.loads(content)

            # Validate and set defaults
            return {
                "summary": analysis.get("summary", "No summary available"),
                "tasks": analysis.get("tasks", []),
                "sentiment": analysis.get("sentiment", "neutral").lower(),
            }

    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        return {
            "summary": f"Analysis completed but parsing failed: {str(e)}",
            "tasks": [],
            "sentiment": "neutral",
        }
    except httpx.HTTPStatusError as e:
        return {
            "summary": f"LLM API error: {e.response.status_code}",
            "tasks": [],
            "sentiment": "neutral",
        }
    except Exception as e:
        return {
            "summary": f"Error analyzing text: {str(e)}",
            "tasks": [],
            "sentiment": "neutral",
        }


