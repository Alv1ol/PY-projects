

from httpx import AsyncClient


async def test_generate_slug(ac: AsyncClient):
    result = await ac.post("/short_url", json={"long_url": "https://my-site.com"})
    assert result.status_code == 200


async def test_redirect_slug(ac: AsyncClient):
    # Сначала создаем короткую ссылку
    create_result = await ac.post("/short_url", json={"long_url": "https://my-site.com"})
    assert create_result.status_code == 200
    # Затем получаем slug из ответа и перенаправляемся
    slug = create_result.json()["data"]
    result = await ac.get(f"/{slug}", follow_redirects=False)
    assert result.status_code == 302
