import requests
# base_uri = 'https://sour-panther-bharatavjo-fca7ad2f.koyeb.app'
base_uri = 'http://localhost:8000'


# First API call to get competitor ads
def get_competitor_ads(company_name, product_name) -> list:
    url = f"{base_uri}/analyze-competitor-ads"
    payload = {"company_name": company_name, "product_name": product_name}
    res = requests.post(url, json=payload, timeout=120)
    res.raise_for_status()
    return res.json()  # Expected to be a list of 5 competitor ad objects


# Second API call to generate creative ideas based on competitor ads
def generate_creative_ideas(competitor_ads, product_name) -> list:
    url = f"{base_uri}/generate-ad-ideas"
    payload = {"competitor_ads": competitor_ads, "product_name": product_name}
    res = requests.post(url, json=payload, timeout=1200)
    res.raise_for_status()
    return res.json()  # Expected to be a list of 5 creative ideas


# Final API calls for customized ad generation
def create_final_ad_text(text_idea, company_name, product_name, custom_text) -> list:
    url = f"{base_uri}/generate-marketing-text"
    payload = {
        "idea": text_idea,
        "company_name": company_name,
        "product_name": product_name,
        "user_input": custom_text,
    }
    res = requests.post(url, json=payload, timeout=60)
    res.raise_for_status()
    return res.json()  # Expected to be the final ad text



# Keeping style hardcode as of now
def create_final_ad_image(image_idea) -> list:
    return {
        "image_url": "https://img.recraft.ai/b6cLjEzfJGPg4fLSwmCV2U_ACzRyTokSrZARSx2fFo8/rs:fit:1024:1024:0/raw:1/plain/abs://external/images/43d92767-b20c-4caf-90be-2e2629d775fa"
    }
    url = f"{base_uri}/ggenerate-marketing-image"
    payload = {"prompt": image_idea, "style": "digital_illustration"}
    res = requests.post(url, json=payload, timeout=60)
    res.raise_for_status()
    return res.json()  # Expected to be the final ad image URL
