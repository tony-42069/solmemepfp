# 🍌 SolMeme Generator

Transform your profile picture into Solana memecoin-themed versions using Google's Gemini 2.5 Flash Image API!

## 🚀 Features

- **9 Solana Memecoin Styles**: WIF, BONK, POPCAT, PENGU, PNUT, MOODENG, CHILLGUY, TRUMP, FARTCOIN
- **Facial Feature Preservation**: Advanced prompting ensures your face remains exactly the same
- **Custom Modifications**: Add your own custom prompts for unique results
- **Auto-save**: Automatically save generated images to the outputs folder
- **Twitter Sharing**: Ready-to-use tweet text for sharing your creations

## 🛠️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tony-42069/solmeme.git
   cd solmeme
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run solmeme_generator.py
   ```

## 🎨 Memecoin Styles

- **🐕 $WIF (Dogwifhat)**: Pink beanie hat, cozy vibes
- **🥜 $BONK (Bonk)**: OG Solana memecoin energy, community vibes
- **🐱 $POPCAT**: Viral cat meme energy, expressive vibes
- **🐧 $PENGU (Pudgy Penguins)**: Cute penguin vibes, wholesome energy
- **🥜 $PNUT (Peanut)**: Squirrel mascot energy, viral story vibes
- **🦛 $MOODENG**: Baby hippo cuteness, Thailand zoo vibes
- **😎 $CHILLGUY**: Laid-back vibes, sunglasses energy
- **🚀 $TRUMP**: Presidential memecoin, political energy
- **💨 $FARTCOIN**: Absurd AI-created chaos energy

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Select `solmeme_generator.py` as the main file
4. Add your `GEMINI_API_KEY` as a secret
5. Deploy!

## 🏗️ Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Google Gemini 2.5 Flash Image Preview API
- **Image Processing**: PIL (Pillow) for image handling
- **Environment**: python-dotenv for secure API key management

## 📝 License

Built for the Nano Banana Hackathon 2025

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 🙏 Acknowledgments

- Google Gemini 2.5 Flash Image API
- Solana memecoin community
- Nano Banana Hackathon organizers
