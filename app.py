import streamlit as st
import random
import json
import os
from PIL import Image
import base64
import streamlit_image_coordinates as sic
import streamlit.components.v1 as components

def get_base64_img(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set page config with centered layout
st.set_page_config(page_title="The Enchanted Cauldron", layout="centered")

# Responsive viewport meta for mobile devices
components.html("""
    <meta name="viewport" content="width=device-width, initial-scale=1">
""", height=0)
# Unified custom CSS block
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Cardo&display=swap');

html, body, .stApp {
    background: linear-gradient(180deg, #1c1b29 0%, #100f18 100%);
    color: #f0e6dd;
    font-family: 'Cardo', serif;
}
.stApp {
    padding: 0 2rem;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'UnifrakturMaguntia', serif;
    color: #ffddb3;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(255, 222, 179, 0.2);
}

/* Button Styling */
.stButton>button {
    border-radius: 6px;
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
    border: 1px solid #f8e9d6 !important;
    box-shadow: 0 0 8px #ffcc99aa;
    transition: box-shadow 0.3s ease;
}
.stButton>button:hover {
    box-shadow: 0 0 12px #ffcc99;
    background-color: #553355 !important;
}

/* Form inputs unified dark theme */
input, select, textarea {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
    border: 1px solid #f8e9d6 !important;
}
.stTextInput>div>input,
.stDateInput input {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
}

/* SelectBox and MultiSelect styling */
.stSelectbox>div>div,
.stMultiSelect>div>div,
.css-1n76uvr, .css-1wa3eu0 {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
    border: 1px solid #f8e9d6 !important;
    border-radius: 4px;
}
div[data-baseweb="select"] {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
    border: 1px solid #f8e9d6 !important;
}
div[data-baseweb="select"] * {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
}

/* Options in multiselect dropdown */
.css-13cymwt-control, .stMultiSelect > div {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
    border: 1px solid #f8e9d6 !important;
    border-radius: 4px !important;
}
.css-1n6sfyn-MenuList, .css-1n6sfyn-option {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
}

/* Focus style for MultiSelect */
.stMultiSelect:focus-within {
    box-shadow: 0 0 0 2px #ffcc99aa;
}

/* Radio Button Styling */
.stRadio > div[role="radiogroup"] label,
.stRadio > div[role="radiogroup"] label span {
    font-weight: 600 !important;
    color: #f8e9d6 !important;
    font-size: 1.05rem !important;
}

/* Labels */
label {
    color: #f0e6dd !important;
}

/* Sidebar & Tabs */
.stSidebar, .css-1d391kg {
    background-color: #1a1824 !important;
    border-right: 1px solid #3b364d;
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: #151422;
    padding-bottom: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    color: #aaa !important;
    font-weight: bold;
    font-size: 1.1rem;
    box-shadow: none !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #ffcc99 !important;
    font-weight: bold !important;
}

/* Miscellaneous spacing & structure */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.stMarkdown {
    font-size: 1.1rem;
}

/* Hide Streamlit header */
header {
    visibility: hidden;
    height: 0;
}
/* Final fix for multiselect dropdown and radio buttons */
div[data-baseweb="select"] {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
    border: 1px solid #f8e9d6 !important;
    border-radius: 4px !important;
}
div[data-baseweb="select"] * {
    background-color: #2a1e3a !important;
    color: #f8e9d6 !important;
}                   

/* Stronger rule to enforce styling on all radio label children */
.stRadio div[role="radiogroup"] * {
    color: #f8e9d6 !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
}

@media screen and (max-width: 768px) {
    html, body, .stApp {
        font-size: 1rem;
        padding: 0.5rem;
    }

    h1, h2, h3 {
        font-size: 1.8rem !important;
    }

    .stButton > button {
        padding: 0.4rem 1rem;
        font-size: 0.95rem;
    }

    .block-container {
        padding: 1rem 0.5rem !important;
    }

    img {
        max-width: 100% !important;
        height: auto;
    }

    .stColumns {
        flex-direction: column !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='padding: 1rem; background-color: #241f35; border-left: 5px solid #1c1b29; margin-bottom: 1rem;'>
    <h1 style='margin: 0;'>The Enchanted Cauldron</h1>
</div>
""", unsafe_allow_html=True)

# INIT STATE
if "show_bat" not in st.session_state:
    st.session_state.show_bat = True

# LOAD DATA
TAROT_FILE = "assets/tarot_cards.json"
SPELLBOOK_FILE = "data/spellbook.json"
CRYSTAL_FILE = "assets/crystals.json"
TAROT_JSON_FILE = "data/tarot.json"
if os.path.exists(TAROT_JSON_FILE):
    with open(TAROT_JSON_FILE, "r") as f:
        tarot_cards = json.load(f)
else:
    tarot_cards = []

if os.path.exists(SPELLBOOK_FILE):
    with open(SPELLBOOK_FILE, 'r') as f:
        spellbook = json.load(f)
else:
    spellbook = []

if os.path.exists(CRYSTAL_FILE):
    with open(CRYSTAL_FILE, 'r') as f:
        crystals = json.load(f)
else:
    crystals = []

# INIT STATE
st.session_state.known_spells = [spell['name'] for spell in spellbook] if spellbook else []

if "game_phase" not in st.session_state:
    st.session_state.game_phase = "idle"  # idle, display, guess

# SIDEBAR NAVIGATION
with st.sidebar:
    st.title("Welcome!")
    st.markdown("""
    A cauldron of mystery and magic awaits! 
      
    Draw tarot cards, reveal omens, light a candle for answers, or summon your familiar. 
                
    Peek into the stars with your birth chart, help villagers in need, forage enchanted forest goods, and decode ancient spells in the Spell Jumble.    
    """)
    with st.expander("Witch's Grimoire"):
        st.markdown("### Your collection of spells.")
        if spellbook:
            for spell in spellbook:
                    st.markdown(f"**{spell['name']}**")
                    st.markdown(f"*{spell['description']}*")
                    st.markdown(f"**Ingredients:** {', '.join(spell['ingredients'])}")

    with open("assets/items/bat.gif", "rb") as f:
        st.image(f.read(), use_container_width=True)

# Set up tab pages
tabs = st.tabs([
    "Witch's Cabin", 
    "The Stars", 
    "Help a Villager", 
    "Magical Supplies",
    "Spell Jumble",
    "Credits"
])

# PAGE 1: WITCH'S CABIN
with tabs[0]:
    text_col, door_col = st.columns([4, 1])

    with text_col:
        st.title("The Witch's Cabin")
        st.markdown("🌟 Welcome, dark one. The shop is open for the night...")
        st.markdown("### Tarot and Omen Reading")
        st.markdown("Draw a tarot card or reveal an omen to see what the universe has in store for you.")

    if tarot_cards and st.button("Draw Tarot Card", key="draw_tarot", use_container_width=True):
        with open("assets/sounds/star.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        components.html(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, height=0)
        st.session_state.drawn_card = random.choice(tarot_cards)

    if "drawn_card" in st.session_state:
        drawn = st.session_state.drawn_card
        card_name = drawn['name']
        card_description = drawn['meaning']
        card_daily = drawn.get('daily_meaning', 'Let the stars guide you today.')
        image_path = f"assets/tarot/{drawn['image']}"
        if os.path.exists(image_path):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(image_path, use_container_width=False, width=200)
                st.caption(card_name)
            with col2:
                st.markdown(f"**{card_name}** — *{card_description}*")
                st.markdown(f"**Daily Message:** {card_daily}")

    if st.button("Reveal Omen", key="omen_main", use_container_width=True):
        with open("assets/sounds/click.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        components.html(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, height=0)
        st.session_state.omen = random.choice([
            "A black cat stares at your door.",
            "The moon is unusually crimson tonight.",
            "An eerie fog creeps under your doorstep...",
            "A raven caws ominously from the rooftop.",
            "A chill runs down your spine as you enter the shop.",
            "You hear whispers in the shadows.",
            "A candle flickers without a breeze.",
            "A strange symbol appears on your door.",
            "You find a feather on your doorstep.",
            "A sudden gust of wind blows through the shop.",
            "You feel a presence watching you.",
            "A mirror reflects something that isn't there.",
            "You hear distant chanting in the night.",
            "A strange scent fills the air, like burning sage.",
            "You find an old coin on the floor.",
            "A spider spins a web in the corner of the room.",
            "A book falls from the shelf without being touched.",
            "You hear a faint bell ringing in the distance.",
            "A shadow moves across the wall, but nothing is there.",
        ])
    if "omen" in st.session_state:
        st.markdown(f"&gt; *{st.session_state.omen}*")


    st.markdown("---")
    # Familiar Summoning Section (First, vertically)
    with st.container():
        st.subheader("Summon Your Familiar")
        st.write("Focus your thoughts. When you're ready, call your familiar from the beyond…")
        with open("data/familiar.json", "r") as f:
            familiars = json.load(f)
        summon_familiar = st.button("Summon Familiar", key="summon_familiar", use_container_width=True)
        if summon_familiar:
            with open("assets/sounds/star.mp3", "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            components.html(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, height=0)
            st.session_state.familiar = random.choice(familiars)
        if "familiar" in st.session_state and st.session_state.familiar:
            f = st.session_state.familiar
            familiar_image_path = f"assets/familiars/{f['name']}.png"
            familiar_name = f['name']
            familiar_species = f['species']
            familiar_trait = f['trait']
            familiar_backstory = f['backstory']
            with st.container():
                if os.path.exists(familiar_image_path):
                    st.image(familiar_image_path, width=250)
                st.markdown(f"**{familiar_name}** the *{familiar_species}* — *{familiar_trait}*")
                st.markdown(f"*{familiar_backstory}*")
    
    st.markdown("---")
    # Candle Divination Section (Second, vertically)
    with st.container():
        st.subheader("Candle Divination")
        st.write("Focus your intent and hold a question in your mind. When you're ready, light the candle...")
        light_candle = st.button("Light the Candle", key="light_candle", use_container_width=True)
        if light_candle:
            with open("assets/sounds/candle.mp3", "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            components.html(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, height=0)
            candle_message = random.choice([
                "The flame flickers violently — a warning or upcoming change.",
                "The wax drips in a spiral — new energy is forming around you.",
                "The candle burns steady and tall — you are on the right path.",
                "A sudden gust nearly snuffs the flame — beware distractions.",
                "The flame splits into two — you are torn between choices.",
                "The candle dances playfully — joy is near.",
                "The wax pools calmly — peace surrounds you.",
                "The flame refuses to light at first — delays may come.",
                "The candle crackles — hidden truths are being revealed.",
                "The flame steadies after a flicker — clarity is approaching."
            ])
            st.session_state.candle_result = ("assets/items/candle1.gif", candle_message)

        # Always show candle image/message if the candle was lit (not just after button press)
        if "candle_result" in st.session_state and st.session_state.candle_result:
            candle_image_path, candle_message = st.session_state.candle_result
            with st.container():
                st.image(candle_image_path, width=250)
                st.markdown(f"*{candle_message}*")

# PAGE 2: REVEAL WHAT IS IN THE STARS
with tabs[1]:
    st.title("Reveal What is in the Stars")

    # Begin two-column layout for vertically stacked inputs and gif ---
    col1, col2 = st.columns([2, 2])

    # Zodiac signs list for selectbox
    zodiac_signs = [
        "♈ Aries", "♉ Taurus", "♊ Gemini", "♋ Cancer", "♌ Leo", "♍ Virgo",
        "♎ Libra", "♏ Scorpio", "♐ Sagittarius", "♑ Capricorn", "♒ Aquarius", "♓ Pisces"
    ]

    # Sun sign calculation function
    def get_sun_sign(date_obj):
        month, day = date_obj.month, date_obj.day
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Pisces"
        return ""

with col1:
    col1.markdown("### Horoscope of the Day")
    zodiac_sign = col1.selectbox("What is your sign?", zodiac_signs, index=0)
    if col1.button("Reveal Horoscope", key="reveal_horoscope"):
        with open("assets/sounds/star.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        components.html(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, height=0)

        st.session_state.horoscope = random.choice([
            "Today is a powerful day to set intentions and embrace your inner truth.",
            "Cosmic energy favors reflection — a good time to revisit old goals.",
            "You may feel a shift in your emotions. Trust your intuition.",
            "The stars suggest unexpected joy may find you today.",
            "Avoid overthinking. Let your spirit lead your actions.",
            "An old flame or friend might resurface — tread carefully.",
            "A breakthrough is near. Stay grounded and open to signs.",
            "Use your creative energy — today favors artistic expression.",
            "You are protected. Let go of the fears that no longer serve you.",
            "Let your kindness ripple — it will return multiplied.",
            "A new opportunity is on the horizon. Be ready to seize it.",
            "Trust your instincts today. They will guide you to clarity.",
            "A small act of kindness will bring unexpected rewards.",
            "The universe is aligning to support your dreams. Take action.",
            "A moment of solitude will bring you the answers you seek.",
            "Your relationships are highlighted today. Nurture them with care.",
            "A chance encounter may lead to a new path. Stay open.",
            "The energy of the day is ripe for transformation. Embrace change.",
            "Your intuition is heightened. Listen closely to your inner voice."
        ])
    if "horoscope" in st.session_state:
        col1.markdown(f"&gt; *{st.session_state.horoscope}*")

    col1.markdown("### Simple Birth Chart Reading")
    import datetime
    today = datetime.date.today()
    min_birthdate = datetime.date(1900, 1, 1)
    birth_date = col1.date_input(
        "Select your birthdate to reveal your star sign",
        value=today,
        min_value=min_birthdate,
        max_value=today,
        key="birth_date_input"
    )

    # Display sun sign after selecting date
    if birth_date:
        sun_sign = get_sun_sign(birth_date)
        col1.markdown(f"🌟 Your **Sun Sign** is **{sun_sign}**.")


# PAGE 3: HELP A VILLAGER  
with tabs[2]:
    st.title("Villager Requests")
    st.markdown("A villager approaches your shop, seeking guidance. How will you help them?")

    if "villager_request" not in st.session_state:
        st.session_state.villager_request = None
    if "villager_result" not in st.session_state:
        st.session_state.villager_result = None
    if "selected_ingredients" not in st.session_state:
        st.session_state.selected_ingredients = []

    left_col, mid_col, right_col = st.columns([1.2, 0.1, 1.7])

    with left_col:
        if st.button("Handle Villager Request"):
            with open("assets/sounds/click.mp3", "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            components.html(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, height=0)
            st.session_state.villager_request = random.choice([
                "I'm in love but they don't see me... Can you help?",
                "I've lost something precious in the woods.",
                "My dreams are haunted by shadows.",
                "I feel cursed. Everything I touch breaks.",
                "A great journey awaits me. What should I know?",
                "I need a potion to protect me from dark spirits.",
                "I seek wisdom to find my true path.",
                "My harvest has failed. Can you bless my crops?",
                "I need a charm to ward off bad luck.",
                "I want to know if my love is true.",
                "I fear a storm is coming. Can you help me prepare?",
                "I need guidance to heal my broken heart.",
                "I seek a spell to bring prosperity to my family.",
                "I need a potion to calm my restless spirit.",
                "I want to know if I will find happiness.",
                "I need a charm to protect my home from evil spirits.",
                "I seek a potion to enhance my intuition.",
                "I need a spell to reveal hidden truths.",
                "I want to know if my dreams will come true."
            ])
            st.session_state.villager_result = None
            st.session_state.selected_ingredients = []
            villager_images = [
                "assets/villagers/villager1.png",
                "assets/villagers/villager2.png",
                "assets/villagers/villager3.png",
                "assets/villagers/villager4.png",
                "assets/villagers/villager5.png",
                "assets/villagers/villager6.png",
                "assets/villagers/villager7.png"
            ]
            st.session_state.villager_img = random.choice(villager_images)

        if st.session_state.villager_request:
            # Interaction radio and logic in left_col
            interaction = st.radio(
                "Look in the Grimoire for Magic Potions.",
                [
                    "Mix a magic potion",
                    "Read their fate",
                    "Send them away"
                ]
            )

            if interaction == "Mix a magic potion":
                all_ingredients = sorted({ing for spell in spellbook for ing in spell["ingredients"]})
                st.session_state.selected_ingredients = st.multiselect(
                    "Choose 3 ingredients:",
                    all_ingredients,
                    key="villager_potion_select",
                    label_visibility="visible"
                )
                if st.button("Brew Potion"):
                    with open("assets/sounds/potion.mp3", "rb") as f:
                        audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode()
                    components.html(f"""
                        <audio autoplay>
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                    """, height=0)
                    if len(st.session_state.selected_ingredients) != 3:
                        st.warning("Please select exactly 3 ingredients.")
                    else:
                        matched_spell = None
                        for spell in spellbook:
                            if set(spell["ingredients"]) == set(st.session_state.selected_ingredients):
                                matched_spell = spell
                                break
                        if matched_spell:
                            st.success(f"You crafted: {matched_spell['name']}")
                            if "image" in matched_spell:
                                img_path = f"assets/spells/{matched_spell['image']}"
                                if os.path.exists(img_path):
                                    st.image(img_path, width=250)
                        else:
                            st.error("That combination doesn't match any known spell.")

            elif interaction == "Read their fate":
                if st.button("Gaze into the Crystal Ball"):
                    with open("assets/sounds/star.mp3", "rb") as f:
                        audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode()
                    components.html(f"""
                        <audio autoplay>
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                    """, height=0)
                    st.session_state.villager_result = random.choice([
                        "A hidden opportunity is close. Follow the signs.",
                        "What you seek will appear under the full moon.",
                        "Your fears mask the truth you already know.",
                        "A stranger will change your path.",
                        "What was lost returns when least expected.",
                        "Your heart knows the answer. Trust it.",
                        "A journey will bring clarity to your doubts.",
                        "The shadows hold secrets. Look deeper.",
                        "A gift from the earth will bring you peace.",
                        "Your love is true, but patience is needed.",
                        "A storm will pass, revealing a brighter dawn.",
                        "Your dreams are a map. Follow them closely.",
                        "A blessing is coming your way. Prepare to receive it.",
                        "The winds of change are blowing. Embrace them.",
                        "Your intuition is strong. Listen to it."
                    ])
                if st.session_state.villager_result:
                    st.success(f"{st.session_state.villager_result}")

            elif interaction == "Send them away":
                st.session_state.villager_result = random.choice([
                    "The villager leaves, disappointed but hopeful.",
                    "You send them away with a warning to be cautious.",
                    "They leave, clutching a charm you gave them.",
                    "The villager departs, their heart heavy with uncertainty.",
                    "You send them off with a cryptic message about their future.",
                    "They walk away, glancing back one last time.",
                    "The shadows thicken as the visitor leaves in silence",
                    "You send them away, but they linger, hoping for more.",
                    "The villager departs, their eyes filled with questions.",
                    "You send them off with a riddle to ponder.",
                    "They leave, but you sense they will return.",
                    "The villager walks away, their heart heavy with doubt."
                ])
                st.success(f"{st.session_state.villager_result}")
                st.session_state.villager_request = None
                st.session_state.villager_result = None
                st.session_state.selected_ingredients = []

    with right_col:
        if st.session_state.villager_request:
            st.markdown(f"""
<div style='padding: 1rem; background-color: #2a1e3a; margin-bottom: 1rem; color: #f0e6dd; text-align: left;'>
    <em>"{st.session_state.villager_request}"</em>
</div>
""", unsafe_allow_html=True)
            if "villager_img" in st.session_state and os.path.exists(st.session_state.villager_img):
                colA, colB = st.columns([1, 1])
                with colB:
                    st.image(st.session_state.villager_img, width=300)

# PAGE 4: GATHER MAGICAL SUPPLIES
with tabs[3]:
    st.title("Gather Magical Supplies")
    st.markdown("The moonlit forest calls. What strange and useful items will you find tonight?")

    # Define all_supplies at the top of this section and initialize gathered_supplies
    all_supplies = [
         "Mandrake root", "Silverleaf fern", "Glowmoss", "Moonstone shard",
         "Bat wing", "Ghost pepper", "Phoenix feather", "Ancient scroll fragment",
         "Crystal vial", "Eyebright flower", "Sage bundle", "Crow’s feather"
    ]

    if "gathered_supplies" not in st.session_state:
        st.session_state.gathered_supplies = []

    st.markdown("Click somewhere in the forest to search for magical supplies:")
    coords = sic.streamlit_image_coordinates("assets/background/forest_search.png", key="forest_map", width=700)
    
    if coords:
        x, y = coords["x"], coords["y"]
        if 50 < x < 200 and 100 < y < 300:
            found = random.choice(all_supplies)
            st.session_state.gathered_supplies.append(found)
            with open("assets/sounds/star.mp3", "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            components.html(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, height=0)
            st.success(f"You found: {found} near the mushrooms!")
        elif 250 < x < 400 and 80 < y < 300:
            found = random.choice(all_supplies)
            st.session_state.gathered_supplies.append(found)
            with open("assets/sounds/star.mp3", "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            components.html(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, height=0)
            st.success(f"You found: {found} by the old tree!")
        elif 450 < x < 600 and 120 < y < 300:
            found = random.choice(all_supplies)
            st.session_state.gathered_supplies.append(found)
            with open("assets/sounds/star.mp3", "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            components.html(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, height=0)
            st.success(f"You found: {found} near the stone arch!")
        else:
            st.info("You searched the forest but found nothing...")

    if st.session_state.gathered_supplies:
        st.markdown("### Your Magical Findings:")
        for item in st.session_state.gathered_supplies:
            st.markdown(f"🔹 {item}")

# PAGE 5: SPELL JUMBLE — UNSCRAMBLE THE ANCIENT SPELL
with tabs[4]:
    st.title("Spell Jumble — Unscramble the Ancient Spell")
    st.markdown("An ancient spell has been uncovered, but its words are scattered like stardust. Can you reassemble its true form?")

    # Load jumbled spells from JSON file
    with open("data/spelljamble.json", "r") as f:
        jumbled_spells = json.load(f)

    if "chosen_spell" not in st.session_state:
        st.session_state.chosen_spell = random.choice(jumbled_spells)
        st.session_state.user_jumble = []

    selected = st.multiselect("Arrange the spell words in the correct order:", st.session_state.chosen_spell["scrambled"], default=st.session_state.user_jumble, key="jumble_input")

    if st.button("Cast the Spell"):
        with open("assets/sounds/spell.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        components.html(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, height=0)
        if " ".join(selected) == st.session_state.chosen_spell["spell"]:
            st.success("The spell has been restored! Ancient magic stirs...")
            st.image("assets/items/pentagram.gif", width=200)
            st.session_state.chosen_spell = random.choice(jumbled_spells)
            st.session_state.user_jumble = []
        else:
            st.error("The spell fizzles... try a different order.")

    if st.button("Try a New Spell"):
        with open("assets/sounds/click.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        components.html(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, height=0)
        st.session_state.chosen_spell = random.choice(jumbled_spells)
        st.session_state.user_jumble = []

# Music Toggle
if "play_music" not in st.session_state:
    st.session_state.play_music = True

# Play music checkbox and custom label style (targeted using Streamlit's data-testid)
play_music = st.sidebar.checkbox("Play background music", key="play_music")
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {
        color: #f5f5f5 !important;
        font-size: 1.1rem !important;
        font-family: 'Cardo', serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.session_state.play_music:
    audio_path = "assets/sounds/background.mp3"
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        components.html(f"""
            <audio autoplay loop>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """, height=0)

# Footer and Credits
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #bbb; font-size: 0.9rem; padding-top: 1rem;'>
    The Enchanted Cauldron — ❤️ Created by Dido De Boodt  
    <br> Background music, illustrations, and magic assets © their respective artists.  
    <br> Contact: <a href="https://www.linkedin.com/in/dido-de-boodt/" target="_blank">LinkedIn</a>
</div>
""", unsafe_allow_html=True)

# Credits & Thanks Tab
with tabs[5]:
    st.title("Credits & Thanks")
    st.markdown("""
    ### Artwork
    - **Tarot Cards**: tarot.com (public domain), artist Pamela Colman Smith  
    - **Familiars & Villagers**: Created by ChatGPT  
    - **Magic Forest Scene**: Created by ChatGPT  
    - **Gifs**: pixabay.com

    ### Sounds 
    • All sound effects and music: Freesound.org contributors under CC-BY license

    ### Fonts
    • UnifrakturMaguntia & Cardo — from Google Fonts

    ### Built with 
    • Python | Streamlit | VS Code 

    Thank you for playing and supporting indie magic! 🌟
    """)