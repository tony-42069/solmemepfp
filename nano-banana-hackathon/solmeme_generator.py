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

        # Memecoin style definitions with simplified prompts to avoid 500 errors
        self.memecoin_styles = {
            "🐕 $WIF (Dogwifhat)": {
                "description": "Pink beanie hat, cozy vibes, dog energy",
                "prompt_template": """Transform this person into Dogwifhat style with a pink beanie hat. Keep their facial features exactly the same."""
            },

            "🥜 $BONK (Bonk)": {
                "description": "OG Solana memecoin energy, community vibes",
                "prompt_template": """Transform this person into BONK style with purple and orange colors. Keep their facial features exactly the same."""
            },

            "🐱 $POPCAT": {
                "description": "Viral cat meme energy, expressive vibes",
                "prompt_template": """Transform this person into POPCAT style with anime-inspired colors. Keep their facial features exactly the same."""
            },

            "🐧 $PENGU (Pudgy Penguins)": {
                "description": "Cute penguin vibes, wholesome energy",
                "prompt_template": """Transform this person into Pudgy Penguins style with winter colors. Keep their facial features exactly the same."""
            },

            "🥜 $PNUT (Peanut)": {
                "description": "Squirrel mascot energy, viral story vibes",
                "prompt_template": """Transform this person into Peanut the Squirrel style with woodland colors. Keep their facial features exactly the same."""
            },

            "🦛 $MOODENG": {
                "description": "Baby hippo cuteness, Thailand zoo vibes",
                "prompt_template": """Transform this person into Moo Deng style with pastel colors. Keep their facial features exactly the same."""
            },

            "😎 $CHILLGUY": {
                "description": "Laid-back vibes, sunglasses energy",
                "prompt_template": """Transform this person into Chill Guy style with sunglasses. Keep their facial features exactly the same."""
            },

            "🚀 $TRUMP": {
                "description": "Presidential memecoin, political energy",
                "prompt_template": """Transform this person into presidential style with American flag colors. Keep their facial features exactly the same."""
            },

            "💨 $FARTCOIN": {
                "description": "Absurd AI-created chaos energy",
                "prompt_template": """Transform this person into FARTCOIN style with chaotic colors. Keep their facial features exactly the same."""
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
        import os
        # Create outputs folder if it doesn't exist
        os.makedirs("outputs", exist_ok=True)
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
