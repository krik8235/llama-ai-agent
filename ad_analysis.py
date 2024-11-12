import json
from together_ai import (
    analyze_product_name,
    validate_with_together_ai,
    idea_from_ad_text_using_together,
    idea_from_ad_image_using_together,
)
from meta_ad_library import search_meta_ads



def fetch_and_analyze_competitor_ads(product_name: str, company_name: str) -> list:
    search_keyword = analyze_product_name(product_name, company_name)
    print("Generated search keyword -> ", search_keyword)

    # meta_ads = search_meta_ads(search_keyword)

    # Loading example ad data
    with open("sample.json", "r", encoding="utf-8") as file:
        meta_ad_response = json.load(file)

    print("Retrieved Meta ads: ", meta_ad_response)
    relevant_ads = []
    continuation_token = meta_ad_response.get("continuation_token")
    MAX_ADS_TO_COLLECT = 5
    print("Analyzing ad content")

    while len(relevant_ads) < MAX_ADS_TO_COLLECT:
        for ad_group in meta_ad_response.get("results", []):
            for ad_data in ad_group:
                try:
                    # Skip ads from the requesting company
                    advertiser_name = ad_data.get("pageName")
                    if advertiser_name == company_name:
                        continue

                    # Extract ad media content
                    ad_snapshot = ad_data.get("snapshot", {})
                    ad_image_url = None

                    # Check primary images array
                    ad_images = ad_snapshot.get("images", [])
                    for image_data in ad_images:
                        ad_image_url = image_data.get("resized_image_url")
                        if ad_image_url:
                            break

                    # Fallback to cards array for image
                    if not ad_image_url:
                        ad_cards = ad_snapshot.get("cards", [])
                        if ad_cards:
                            first_card = ad_cards[0]
                            ad_image_url = first_card.get("resized_image_url")

                    if not ad_image_url:
                        continue

                    # Extract ad copy text
                    ad_body = ad_snapshot.get("body", {})
                    ad_markup = ad_body.get("markup", {})
                    ad_copy = ad_markup.get("__html")

                    if not ad_copy:
                        continue

                    # Validate ad relevance
                    if validate_with_together_ai(ad_copy, search_keyword):
                        relevant_ads.append(
                            {
                                "image_url": ad_image_url,
                                "text": ad_copy,
                                "page_name": advertiser_name,
                            }
                        )
                        print(
                            f"Found relevant ad #{len(relevant_ads)} from advertiser {advertiser_name}"
                        )

                        if len(relevant_ads) >= MAX_ADS_TO_COLLECT:
                            break

                except KeyError as e:
                    print(f"Skipping malformed ad data: {e}")
                    continue

            if len(relevant_ads) >= MAX_ADS_TO_COLLECT:
                break

        if len(relevant_ads) >= MAX_ADS_TO_COLLECT or not continuation_token:
            break

        # Fetch next page of results if needed
        if continuation_token:
            meta_ad_response = search_meta_ads(
                meta_ad_response["query"], continuation_token
            )
            continuation_token = meta_ad_response.get("continuation_token")
            if not meta_ad_response.get("results"):
                print("Retrying fetch due to empty response")
                meta_ad_response = search_meta_ads(
                    meta_ad_response["query"], continuation_token
                )

    print("Ad analysis complete")
    print("Collected ads: ", relevant_ads)
    return relevant_ads


def generate_ad_ideas(competitor_ads: list, product_name: str) -> list:
    ad_ideas = []

    for ad in competitor_ads:
        generate_text_idea = idea_from_ad_text_using_together(ad["text"], product_name)
        print("Generated text idea -> ", generate_text_idea)
        generate_image_idea = idea_from_ad_image_using_together(
            ad["image_url"], product_name
        )
        print("Generated image idea -> ", generate_image_idea)
        ad_ideas.append(
            {
                "ad_text": ad["text"],
                "image_url": ad["image_url"],
                "text_prompt": generate_text_idea,
                "image_prompt": generate_image_idea,
            }
        )

    return ad_ideas
