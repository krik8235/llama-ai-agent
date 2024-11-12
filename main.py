import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from together_ai import analyze_product_name, generate_text_for_marketing_post
from meta_ad_library import search_meta_ads
from dotenv import load_dotenv
from ad_analysis import fetch_and_analyze_competitor_ads, generate_ad_ideas
from generate_image import generate_marketing_ad_image
load_dotenv(override=True)
app = FastAPI()


class CompetitorAdRequest(BaseModel):
    product_name: str
    company_name: str


class CompetitorAdResponse(BaseModel):
    ads: list


class AdIdeaRequest(BaseModel):
    competitor_ads: list
    product_name: str


class AdIdeaResponse(BaseModel):
    ad_ideas: list


# Example curl command:
"""
curl -X POST http://localhost:8000/analyze-competitor-ads \
  -H "Content-Type: application/json" \
  -d '{"product_name": "smartphone", "company_name": "TechCo"}'
"""


@app.post("/analyze-competitor-ads")
async def analyze_competitor_ads(request: CompetitorAdRequest):
    try:
        ads_data = fetch_and_analyze_competitor_ads(
            request.product_name, request.company_name
        )
        return CompetitorAdResponse(ads=ads_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Example curl command:
"""
curl -X POST http://localhost:8000/generate-ad-ideas \
  -H "Content-Type: application/json" \
  -d '{"competitor_ads": [{"text": "ad text", "image_url": "http://example.com/image.jpg"}], "product_name": "smartphone"}'
"""


@app.post("/generate-ad-ideas")
async def generate_ideas(request: AdIdeaRequest):
    try:
        ad_ideas = generate_ad_ideas(request.competitor_ads, request.product_name)
        return AdIdeaResponse(ad_ideas=ad_ideas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ImageGenerationRequest(BaseModel):
    prompt: str
    style: str = "digital_illustration"


class ImageGenerationResponse(BaseModel):
    image_url: str | None


# Example curl command:
"""
curl -X POST http://localhost:8000/generate-marketing-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A modern smartphone with sleek design", "style": "digital_illustration"}'
"""


@app.post("/generate-marketing-image")
async def generate_marketing_image(request: ImageGenerationRequest):
    try:
        # Generate image with 15 second timeout
        async with asyncio.timeout(15):
            image_url = await asyncio.to_thread(
                generate_marketing_ad_image, request.prompt, request.style
            )
            if not image_url:
                raise HTTPException(status_code=500, detail="Failed to generate image")
            return ImageGenerationResponse(image_url=image_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MarketingTextRequest(BaseModel):
    idea: str
    company_name: str
    product_name: str
    user_input: str | None = None  # Making user_input optional


class MarketingTextResponse(BaseModel):
    marketing_text: str


# Example curl command:
"""
curl -X POST http://localhost:8000/generate-marketing-text \
  -H "Content-Type: application/json" \
  -d '{"idea": "Focus on innovation", "company_name": "TechCo", "product_name": "smartphone", "user_input": "Emphasize AI features"}'
"""


@app.post("/generate-marketing-text")
async def generate_marketing_text(request: MarketingTextRequest):
    try:
        marketing_text = generate_text_for_marketing_post(
            idea=request.idea,
            company_name=request.company_name,
            product_name=request.product_name,
            user_input=request.user_input,
        )
        return MarketingTextResponse(marketing_text=marketing_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
