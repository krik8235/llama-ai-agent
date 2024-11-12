import requests
import os
from dotenv import load_dotenv


load_dotenv()


def generate_image(
    prompt,
    style,
    n=1,
    style_id=None,
    substyle=None,
    response_format="url",
    size="1024x1024",
    controls=None,
):
    """
    Generate an image using Recraft AI API.

    Args:
        prompt (str): Text description of desired image (max 500 chars)
        style (str, optional): Style of generated images. Defaults to 'realistic_image'
        n (int, optional): Number of images to generate (1 or 2). Defaults to 1
        style_id (str, optional): UUID of previously uploaded style. Mutually exclusive with style
        substyle (str, optional): Substyle parameter for additional style control
        response_format (str, optional): Format of response - 'url' or 'b64_json'. Defaults to 'url'
        size (str, optional): Size of generated images in WxH format. Defaults to '1024x1024'
        controls (dict, optional): Custom parameters to tweak generation process

    Returns:
        Response object containing generated image data
    """
    # API endpoint
    url = "https://external.api.recraft.ai/v1/images/generations"

    # Headers
    headers = {
        "Authorization": f'Bearer {os.getenv("RECRAFT_API_KEY")}',
        "Content-Type": "application/json",
    }

    # Build request body
    request_body = {
        "prompt": prompt,
        "n": n,
        "response_format": response_format,
        "size": size,
    }

    # Add optional parameters if provided
    if style_id:
        request_body["style_id"] = style_id
    elif style:
        request_body["style"] = style

    if substyle:
        request_body["substyle"] = substyle

    if controls:
        request_body["controls"] = controls

    # Make API call
    try:
        response = requests.post(url, headers=headers, json=request_body, timeout=15)
        response.raise_for_status()  # Raise exception for error status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating image: {str(e)}")
        return None


def generate_marketing_ad_image(
    prompt: str, style: str = "digital_illustration"
) -> str:
    """
    Generates a marketing ad image using the Recraft AI API

    Args:
        prompt (str): Description of the marketing ad to generate
        style (str, optional): Style of the generated image. Defaults to 'digital_illustration'

    Returns:
        str: URL of the generated image, or None if generation failed
    """
    size = "1024x1024"  # High resolution square image

    # Default controls for high quality marketing ads
    controls = {
        "quality": "high",
        "composition": "centered",
        "style_strength": "high",
    }
    response = generate_image(
        prompt=prompt,
        style=style,
        size=size,
        controls=controls,
        n=1,  # Generate single image
    )

    if response and "data" in response:
        image_data = response["data"][0]
        if "url" in image_data:
            return image_data["url"]

    return None
