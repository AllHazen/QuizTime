import streamlit as st
import time
import base64

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Quiz Time", page_icon="🕒")
st.title("Quiz Time! 🕒")

# --- Inisialisasi session_state ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False
if "typed_questions" not in st.session_state:
    st.session_state.typed_questions = set()
if "final_shown" not in st.session_state:
    st.session_state.final_shown = False
if "no_pressed" not in st.session_state:
    st.session_state.no_pressed = False

# Flag pemutar suara setelah rerun
if "play_sound" not in st.session_state:
    st.session_state.play_sound = False
if "play_sound_file" not in st.session_state:
    st.session_state.play_sound_file = None

# --- Daftar pertanyaan ---
math_questions = [
    ("Berapakah hasil dari 5 × 3?", "15", "12", "15"),
    ("Jika 2x + 4 = 10, maka nilai x adalah?", "2", "3", "3"),
    ("Berapakah hasil dari 12 ÷ 4?", "4", "3", "3"),
    ("Jika y² = 16, maka nilai y adalah?", "4", "8", "4"),
]

final_question = "So... the last question is... 💕\nWill you be my Pre Order girlfriend? 💍"

# --- Fungsi efek mengetik ---
def typing_effect(text, delay=0.03, icon="🤖 Chatbot"):
    placeholder = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(f"**{icon}:** {typed_text}▌")
        time.sleep(delay)
    placeholder.markdown(f"**{icon}:** {typed_text}")

# konverter file ke base64 untuk HTML autoplay
def convert_to_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def play_sound_autoplay_html(file_path):
    """Sisipi HTML autoplay berbasis base64 (eksperimental, browser mungkin blokir)."""
    b64 = convert_to_base64(file_path)
    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- Tampilkan percakapan sebelumnya ---
for sender, msg in st.session_state.messages:
    if sender == "Wina":
        st.markdown(f"**🧍‍♀️ Wina:** {msg}")
    elif sender == "Chatbot":
        st.markdown(f"**🤖 Chatbot:** {msg}")
    elif sender == "image":
        # tampilkan gambar lokal/gif
        st.image(msg, width=250)

# --- Intro sebelum kuis dimulai ---
if not st.session_state.intro_done:
    intro_lines = [
        "Hai Wina...",
        "Waktunya tiba-tiba Quiz Time! 😄",
        "Kamu siap? 😏",
    ]

    # Tampilkan intro dengan efek mengetik hanya sekali
    if not any(msg in intro_lines for sender, msg in st.session_state.messages):
        for line in intro_lines:
            typing_effect(line)
            st.session_state.messages.append(("Chatbot", line))
            time.sleep(0.4)

    if st.button("Mulai Kuis 💫"):
        st.session_state.intro_done = True
        st.session_state.started = True
        st.session_state.messages.append(("Chatbot", "Langsung mulai! 🚀"))
        st.rerun()

# --- Jika kuis sudah dimulai dan masih ada soal ---
elif st.session_state.started and st.session_state.step < len(math_questions):
    q, a1, a2, correct = math_questions[st.session_state.step]

    # Efek mengetik hanya sekali per pertanyaan
    if st.session_state.step not in st.session_state.typed_questions:
        st.session_state.typed_questions.add(st.session_state.step)
        typing_effect(q)
    else:
        st.markdown(f"**🤖 Chatbot:** {q}")

    # Tombol jawaban pilihan ganda
    col1, col2 = st.columns(2)
    with col1:
        if st.button(a1, key=f"a1_{st.session_state.step}"):
            st.session_state.messages.append(("Wina", a1))
            if a1 == correct:
                st.session_state.messages.append(("Chatbot", "✅ Benar sekali! 😍"))
                st.session_state.messages.append(("image", "cat.gif"))
                # tandai untuk mainkan suara setelah rerun
                st.session_state.play_sound = True
                st.session_state.play_sound_file = "happy_happy_cat.mp3"
                st.session_state.step += 1
            else:
                st.session_state.messages.append(("Chatbot", "❌ Coba lagi say 😉"))
                st.session_state.messages.append(("image", "the-voices.gif"))
            st.rerun()
    with col2:
        if st.button(a2, key=f"a2_{st.session_state.step}"):
            st.session_state.messages.append(("Wina", a2))
            if a2 == correct:
                st.session_state.messages.append(("Chatbot", "✅ Kerja Bagus ❤️"))
                st.session_state.messages.append(("image", "cat.gif"))
                st.session_state.play_sound = True
                st.session_state.play_sound_file = "happy_happy_cat.mp3"
                st.session_state.step += 1
            else:
                st.session_state.messages.append(("Chatbot", "❌ Hmm, belum benar nih 😅"))
                st.session_state.messages.append(("image", "the-voices.gif"))
            st.rerun()

# --- Pertanyaan terakhir ---
elif st.session_state.step == len(math_questions):
    if not st.session_state.final_shown:
        typing_effect(final_question, delay=0.03)
        st.session_state.final_shown = True
    else:
        st.markdown(f"**🤖 Chatbot:** {final_question}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes 💕"):
            st.session_state.messages.append(("Wina", "Yes 💕"))
            st.session_state.messages.append(("Chatbot", "🥰 Horee! ❤️"))
            st.session_state.messages.append(("image", "cat.gif"))
            st.session_state.play_sound = True
            st.session_state.play_sound_file = "happy_happy_cat.mp3"
            st.session_state.step += 1
            st.rerun()

    if not st.session_state.no_pressed:
        with col2:
            if st.button("No 😢"):
                st.session_state.messages.append(("Wina", "No 😢"))
                st.session_state.messages.append(("Chatbot", "😢 kok No... ulang yaw..."))
                st.session_state.no_pressed = True
                st.rerun()

# --- Setelah semua selesai ---
else:
    st.markdown("**🤖 Chatbot:** dah PO coyy 💞")

# --- Mainkan suara setelah rerun jika diminta ---
if st.session_state.play_sound and st.session_state.play_sound_file:
    # 1) tampilkan audio player (user bisa klik Play)
    try:
        with open(st.session_state.play_sound_file, "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
    except FileNotFoundError:
        st.error(f"File suara '{st.session_state.play_sound_file}' tidak ditemukan.")

    # 2) coba sisipkan HTML autoplay (eksperimental; browser mungkin tetap blokir)
    try:
        play_sound_autoplay_html(st.session_state.play_sound_file)
    except Exception:
        pass

    # reset flag supaya tidak berulang
    st.session_state.play_sound = False
    st.session_state.play_sound_file = None
