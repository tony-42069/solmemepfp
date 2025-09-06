"""
SolMeme Generator - Transform Your PFP into Solana Memecoin Vibes
The ultimate tool for Solana memecoin Twitter
"""

import os
import streamlit as st
from google import genai
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

class SolMemeGenerator:
    def __init__(self):
        """Initialize the SolMeme Generator with API client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Please set GEMINI_API_KEY in your .env file or Streamlit secrets")
            # Don't return - still initialize memecoin_styles for UI
            self.client = None
            self.model = "gemini-2.5-flash-image-preview"
        else:
            self.client = genai.Client(api_key=api_key)
            self.model = "gemini-2.5-flash-image-preview"

        # Memecoin style definitions with professional prompts
        self.memecoin_styles = {
            "🐕 $WIF (Dogwifhat)": {
                "description": "Pink beanie hat, cozy vibes, dog energy",
                "prompt_template": """Transform this person into Dogwifhat style with a pink beanie hat. Keep their facial features exactly the same."""
            },

            "🥜 $BONK (Bonk)": {
                "description": "OG Solana memecoin energy, community vibes",
                "prompt_template": """Using the provided profile picture, transform this person into the BONK ($BONK) memecoin aesthetic while ensuring their facial features, expression, and bone structure remain completely unchanged.

Add subtle Solana-themed elements: incorporate purple and orange color accents in the background or clothing. The person should have an energetic, optimistic expression (while keeping their natural facial features). Add soft purple/orange lighting that enhances the scene without changing the person's appearance.

Include small BONK-style elements like playful sparkles or subtle geometric patterns in the background. The overall mood should be enthusiastic and community-focused, representing the OG Solana memecoin spirit. Preserve all original lighting and composition."""
            },

            "🐱 $POPCAT": {
                "description": "Viral cat meme energy, expressive vibes",
                "prompt_template": """Using the provided profile picture, transform this person into the POPCAT ($POPCAT) aesthetic while preserving their exact facial features and bone structure completely unchanged.

Enhance the image with vibrant, slightly anime-inspired lighting and colors. Add large, expressive eyes effect (while keeping their natural eye color and shape). The background should feature bright, cheerful colors with subtle cat-themed elements or patterns.

The overall style should be energetic and viral-ready, capturing the playful spirit of the POPCAT meme. Use dynamic lighting that makes the image pop with color and energy, while ensuring the person's actual face remains unchanged."""
            },

            "🐧 $PENGU (Pudgy Penguins)": {
                "description": "Cute penguin vibes, wholesome energy",
                "prompt_template": """Using the provided profile picture, transform this person into the Pudgy Penguins ($PENGU) aesthetic while keeping their facial features, expression, and bone structure exactly the same.

Add subtle penguin-inspired elements: a cozy winter background with soft blues and whites. The person could be wearing a cute winter accessory like a scarf or hat in penguin colors (black, white, orange accents). The overall mood should be wholesome, cute, and family-friendly.

Create a warm, inviting atmosphere with soft lighting that enhances the adorable, community-focused vibe of Pudgy Penguins. Ensure all facial details remain completely preserved from the original image."""
            },

            "🥜 $PNUT (Peanut)": {
                "description": "Squirrel mascot energy, viral story vibes",
                "prompt_template": """Using the provided profile picture, transform this person into the Peanut the Squirrel ($PNUT) aesthetic while ensuring their facial features and expression remain completely unchanged.

Add elements inspired by the viral squirrel story: natural, outdoor-inspired background with warm brown and golden tones. Include subtle woodland or nature elements. The person should have a determined, resilient expression (while maintaining their natural features).

The lighting should be warm and golden, representing strength and community support. Add small acorn or nut elements in the background as subtle nods to the PNUT theme. Preserve all original facial characteristics while enhancing the inspirational, story-driven mood."""
            },

            "🦛 $MOODENG": {
                "description": "Baby hippo cuteness, Thailand zoo vibes",
                "prompt_template": """Using the provided profile picture, transform this person into the Moo Deng ($MOODENG) aesthetic while preserving their exact facial features, bone structure, and expression unchanged.

Create a cute, playful atmosphere inspired by the viral baby hippo. Use soft, rounded elements and gentle pastel colors. The background should evoke a peaceful, zoo-like or natural water environment with soft blues and greens.

Add adorable, rounded design elements that echo the baby hippo's charm while maintaining a photorealistic quality. The lighting should be soft and natural, creating an atmosphere of pure cuteness and innocence. Ensure the person's face remains exactly as in the original."""
            },

            "😎 $CHILLGUY": {
                "description": "Laid-back vibes, sunglasses energy",
                "prompt_template": """Using the provided profile picture, transform this person into the Chill Guy ($CHILLGUY) aesthetic while keeping their facial features and bone structure completely unchanged.

Add stylish sunglasses that fit naturally on their face. Create a relaxed, tropical or beach-inspired background with soft, warm colors. The overall mood should be laid-back, confident, and effortlessly cool.

Use golden hour lighting that creates a chill, vacation-like atmosphere. Add subtle elements like palm trees or beach elements in the soft-focus background. The person should embody the "just chilling" energy while maintaining their natural facial characteristics and expression."""
            },

            "🚀 $TRUMP": {
                "description": "Presidential memecoin, political energy",
                "prompt_template": """Using the provided profile picture, transform this person into the Official Trump ($TRUMP) memecoin aesthetic while ensuring their facial features and expression remain exactly the same.

Add patriotic elements: American flag colors in the background, presidential or official styling. The lighting should be professional and confident, like a formal portrait. Use red, white, and blue color accents throughout the scene.

Create a powerful, presidential atmosphere with clean, professional composition. The background can include subtle stars or stripes patterns. Maintain the dignity and formality appropriate for a political-themed memecoin while preserving all original facial features."""
            },

            "💨 $FARTCOIN": {
                "description": "Absurd AI-created chaos energy",
                "prompt_template": """Using the provided profile picture, transform this person into the FARTCOIN ($FARTCOIN) aesthetic while keeping their facial features completely unchanged.

Create a chaotic, absurd, and humorous atmosphere with wild colors and unexpected elements. Use neon colors, glitch effects, or surreal background elements that capture the AI-generated randomness of FARTCOIN.

The overall mood should be deliberately absurd and meme-heavy, embracing the chaos of the most ridiculous memecoin. Add colorful, explosive visual effects while ensuring the person's actual face and features remain exactly as in the original image. Make it wonderfully weird and viral-ready."""
            }
        }

    def generate_pfp(self, uploaded_image, selected_style, custom_prompt=""):
        """Generate a memecoin-styled PFP using Nano Banana"""
        try:
            # Check if client is available
            if self.client is None:
                return None, "API key not configured. Please check your Streamlit secrets."

            # Get the style template
            style_data = self.memecoin_styles[selected_style]
            base_prompt = style_data["prompt_template"]

            # Add custom modifications if provided
            if custom_prompt:
                base_prompt += f"\n\nAdditional modifications: {custom_prompt}"

            # Debug logging
            print(f"🔍 Using prompt (length: {len(base_prompt)} chars)")
            print(f"🎨 Style: {selected_style}")

            # Generate the image
            response = self.client.models.generate_content(
                model=self.model,
                contents=[base_prompt, uploaded_image]
            )

            # Extract image from response
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    generated_image = Image.open(BytesIO(part.inline_data.data))
                    return generated_image, "Success!"
                elif part.text is not None:
                    st.write(f"AI Response: {part.text}")

            return None, "No image generated in response"

        except Exception as e:
            # Enhanced error logging
            error_msg = str(e)
            print(f"❌ Error: {error_msg}")
            print(f"Error type: {type(e).__name__}")

            # Check for specific error types
            if "500" in error_msg:
                return None, "Server error (500). The API may be experiencing issues. Please try again in a few minutes."
            elif "429" in error_msg:
                return None, "Rate limit exceeded. Please wait a moment before trying again."
            elif "403" in error_msg:
                return None, "Access denied. Please check your API key and permissions."
            else:
                return None, f"Error generating image: {error_msg}"

    def save_image(self, image, filename):
        """Save generated image to outputs folder"""
        output_path = f"outputs/{filename}"
        image.save(output_path)
        return output_path

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="SolMeme Generator",
        page_icon="🍌",
        layout="wide"
    )

    # Header
    st.title("🍌 SolMeme Generator")
    st.subheader("Transform Your PFP into Solana Memecoin Vibes")
    st.write("Upload your profile picture and choose your Solana memecoin aesthetic!")

    # Initialize the generator
    generator = SolMemeGenerator()

    # Sidebar for controls
    with st.sidebar:
        st.header("🎨 Choose Your Vibe")

        # Style selection
        selected_style = st.selectbox(
            "Select Memecoin Style:",
            list(generator.memecoin_styles.keys()),
            help="Choose which Solana memecoin aesthetic you want"
        )

        # Show style description
        if selected_style:
            style_info = generator.memecoin_styles[selected_style]
            st.info(f"**Style:** {style_info['description']}")

        # Custom modifications
        st.header("✨ Custom Tweaks")
        custom_prompt = st.text_area(
            "Additional modifications (optional):",
            placeholder="e.g., 'make it more colorful', 'add galaxy background', 'more intense lighting'",
            help="Add specific requests to customize your PFP further"
        )

        # Generation settings
        st.header("⚙️ Settings")
        auto_save = st.checkbox("Auto-save generated images", value=True)

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📸 Upload Your PFP")

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose your profile picture",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear profile picture for best results"
        )

        if uploaded_file is not None:
            # Display uploaded image
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Your Original PFP", use_column_width=True)

            # Generate button
            if st.button("🚀 Generate SolMeme PFP", type="primary"):
                with st.spinner("Creating your memecoin vibe..."):
                    generated_image, message = generator.generate_pfp(
                        uploaded_image,
                        selected_style,
                        custom_prompt
                    )

                    if generated_image:
                        st.session_state.generated_image = generated_image
                        st.session_state.generation_message = message

                        # Auto-save if enabled
                        if auto_save:
                            filename = f"solmeme_{selected_style.split()[1].replace('$', '').replace('(', '').replace(')', '')}_pfp.png"
                            saved_path = generator.save_image(generated_image, filename)
                            st.success(f"Generated and saved to: {saved_path}")
                        else:
                            st.success(message)
                    else:
                        st.error(message)

    with col2:
        st.header("✨ Your SolMeme PFP")

        # Display generated image
        if 'generated_image' in st.session_state:
            st.image(
                st.session_state.generated_image,
                caption=f"Your {selected_style} PFP",
                use_column_width=True
            )

            # Download button
            img_buffer = BytesIO()
            st.session_state.generated_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            st.download_button(
                label="💾 Download Your PFP",
                data=img_buffer.getvalue(),
                file_name=f"solmeme_pfp_{selected_style.split()[1].replace('$', '')}.png",
                mime="image/png"
            )

            # Social sharing text
            st.subheader("📱 Share on Twitter")
            tweet_text = f"Just transformed my PFP with SolMeme Generator! {selected_style} vibes 🔥 #SolanaMemecoin #NanaBananaHackathon"
            st.code(tweet_text)

        else:
            st.info("Upload an image and hit generate to see your SolMeme PFP here!")

            # Preview gallery
            st.subheader("🎨 Style Preview")
            st.write("Here's what each style brings to your PFP:")

            for style_name, style_data in generator.memecoin_styles.items():
                with st.expander(f"{style_name}"):
                    st.write(f"**Vibe:** {style_data['description']}")

    # Footer
    st.markdown("---")
    st.markdown(
        "**Built for the Nano Banana Hackathon** | "
        "Powered by Gemini 2.5 Flash Image Preview | "
        "Made for the Solana memecoin community 🚀"
    )

if __name__ == "__main__":
    main()
