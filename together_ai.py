import os
import json
from dotenv import load_dotenv
from typing import Literal
from together import Together
from pydantic import BaseModel, Field
load_dotenv(override=True)
together = Together(api_key=os.getenv('TOGETHER_API_KEY'))


class AnalysisResult(BaseModel):
    keyword: str = Field(
        description="A keyword generated from the product name analysis."
    )


class RelevanceResponse(BaseModel):
    is_relevant: Literal["yes", "no"] = Field(
        description="Indicates whether the ad text is relevant to the keyword",
        examples=["yes", "no"],
    )

    class Config:
        json_schema_extra = {"example": {"is_relevant": "yes"}}


class AdvertisementIdea(BaseModel):
    idea_of_ad: str = Field(
        ...,
        min_length=200,
        max_length=400,
        description="Template-style advertising concept that can be adapted for different products",
    )

class AdvertisementText(BaseModel):
    advertisement_text: str = Field(
        description="The final generated marketing advertisement post for the product or service",
    )


def analyze_text(
    prompt: str, schema, model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
) -> str:
    """Generalized function to call Together AI with a prompt and return a JSON response."""
    extract = together.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Analyze the input text and respond in JSON format.",
            },
            {"role": "user", "content": prompt},
        ],
        model=model,
        response_format={"type": "json_object", "schema": schema.model_json_schema()},
    )

    output = json.loads(extract.choices[0].message.content)
    return output


def analyze_text_image(
    prompt: str,
    image_url: str,
    schema,
    model: str = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
) -> str:
    """Generalized function to call Together AI with a prompt and return a JSON response."""
    print(prompt, image_url, schema)
    extract = together.chat.completions.create(
        messages=[
            # {"role": "system", "content": "Analyze the input text and image and respond in JSON format."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            },
        ],
        model=model,
        # response_format={"type": "json_object", "schema": schema.model_json_schema()},
    )
    # print(extract)
    output = extract.choices[0].message.content
    return output


def idea_from_ad_text_using_together(text: str, product_name: str) -> str:
    prompt = f"""Analyze the reference advertisement text: {text}
    For {product_name}, extract the advertising pattern used focusing on:
    - Text structure and tone
    - Announcement style
    - Promotional language and approach
    - Key messaging elements
    Generate a template-style idea that explains how to adapt this text pattern while maintaining the same impact."""

    result = analyze_text(prompt, AdvertisementIdea)
    return result


def idea_from_ad_image_using_together(image_url: str, product_name: str) -> str:
    prompt = f"""For {product_name}, analyze this reference advertisement image focusing on:
    - Overall visual composition
    - Product positioning
    - Image-to-text ratio and layout
    - Visual style and elements
    Generate a template-style idea that explains how to adapt this visual pattern while maintaining the same impact. limit this under 500 characters."""

    result = analyze_text_image(prompt, image_url, AdvertisementIdea)
    return result


def generate_text_for_marketing_post(
    idea: str, company_name: str, product_name: str, user_input: str = ""
) -> str:
    """
    Generate a marketing post based on the idea, company details and optional user input.

    Args:
        idea (str): The core idea/concept for the marketing post
        company_name (str): Name of the company
        product_name (str): Name of the product
        user_input (str): Optional additional requirements or preferences for the post

    Returns:
        str: Generated marketing post content
    """
    # Build the prompt incorporating all inputs
    prompt = f"""Generate a compelling marketing post for {product_name} by {company_name}.

Core idea to incorporate: {idea}

Guidelines:
- Create engaging, conversion-focused copy
- Maintain brand voice and professionalism
- Include a clear call-to-action
- Keep the message concise and impactful"""

    # Add user input if provided
    if user_input:
        prompt += f"\n\nAdditional Requirements:\n{user_input}"

    result = analyze_text(prompt, AdvertisementText)
    return result["advertisement_text"]


def analyze_product_name(product_name: str, company_name: str) -> str:
    """Generates a search keyword based on product name analysis."""
    prompt = f"Generate a short keyword phrase that represents the product: {product_name}. Company name, any adjective or any superlative should not be present in keyword, remove company name {company_name}"
    result = analyze_text(prompt, AnalysisResult)
    return result["keyword"]


def validate_with_together_ai(ad_text, query):
    prompt = f""" Analyze if the following Meta ad text is related to the keyword: {query}

    Ad Text:
    {ad_text}

    Guidelines for analysis:
    1. Check if the text directly mentions the keyword or its close variations
    2. Look for semantic relationships between the text content and the keyword
    3. Consider the context and intended audience of the ad
    4. Analyze if the ad's message or product/service is related to the keyword theme

    Based on the above analysis, determine if the text is relevant to the keyword.
    Provide only a single word response: 'yes' or 'no'

    Response: """

    response = analyze_text(prompt, RelevanceResponse)

    # Here, replace with actual Together AI API call logic
    # For demonstration, let's assume it returns True if ad_text contains the query term.
    return response["is_relevant"]
