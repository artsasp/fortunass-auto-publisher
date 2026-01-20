"""AI image generation using DALL-E 3."""

import os
import requests
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


class ImageGenerator:
    """Generate images using OpenAI DALL-E 3."""

    def __init__(self, api_key=None, logger=None):
        """Initialize image generator.

        Args:
            api_key: OpenAI API key
            logger: Logger instance
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")

        self.client = OpenAI(api_key=self.api_key)
        self.logger = logger

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def generate_image(self, topic):
        """Generate image for given topic.

        Args:
            topic: Dict with mbti, love_situation, tarot_card, tarot_korean

        Returns:
            Dict with image_url and image_data (bytes)
        """
        if self.logger:
            self.logger.info("Generating image with DALL-E 3")

        # Create prompt for image
        prompt = self._create_image_prompt(topic)

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            image_url = response.data[0].url

            # Download image
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()
            image_data = image_response.content

            if self.logger:
                self.logger.info("Image generated successfully", url=image_url)

            return {
                "url": image_url,
                "data": image_data
            }

        except Exception as e:
            if self.logger:
                self.logger.error(f"Image generation failed: {str(e)}")
            raise

    def _create_image_prompt(self, topic):
        """Create DALL-E prompt from topic.

        Args:
            topic: Topic dictionary

        Returns:
            Image generation prompt
        """
        mbti = topic['mbti']
        tarot_card = topic['tarot_card']
        tarot_korean = topic['tarot_korean']

        # Create artistic, symbolic prompt
        prompt = f"""A beautiful, artistic illustration representing the tarot card '{tarot_card}' ({tarot_korean})
combined with the concept of love and relationships for {mbti} personality type.
The image should be symbolic, mystical, and aesthetic with soft colors and romantic atmosphere.
Include tarot card imagery, abstract symbols of love and emotion, and a dreamy background.
Style: modern digital art, artistic, ethereal, romantic. No text or words in the image."""

        return prompt
