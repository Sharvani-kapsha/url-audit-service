from app.cache import cache
import time
import httpx
from bs4 import BeautifulSoup

async def audit_url(url: str):

    if url in cache:
        result = cache[url].copy()
        result["cached"] = True
        return result

    try:
        start = time.time()

        async with httpx.AsyncClient(
            timeout=5,
            follow_redirects=True
        ) as client:

            response = await client.get(url)

        elapsed = round((time.time() - start) * 1000)

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No Title"

        result = {
            "url": url,
            "status_code": response.status_code,
            "response_time_ms": elapsed,
            "title": title,
            "success": 200 <= response.status_code < 400,
            "cached": False
        }

        cache[url] = result

        return result

    except httpx.TimeoutException:
        return {
            "error": "Request timed out",
            "url": url,
            "success": False
        }

    except httpx.RequestError as e:
        return {
            "error": str(e),
            "url": url,
            "success": False
        }

    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }