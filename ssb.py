import streamlit as st
import time
import base64
import os

# --- CONFIGURATION & SETUP ---

# Folder paths
PPDT_FOLDER_PATH = "ppdt"  # Folder containing PPDT_1.jpg, PPDT_2.jpg, etc.
GPE_MAP_PATH = "GPE_1.jpg"
STOP_SOUND_PATH = "buzzer-buzz-single-sound-effects.mp3"

# PPDT Time Constants (in seconds)
PPDT_VIEW_TIME = 30
PPDT_WRITING_TIME = 5 * 60
TOTAL_PPDT_TIME = PPDT_VIEW_TIME + PPDT_WRITING_TIME

# GPE Narration/Problem Statement
GPE_NARRATION = """
You are a group of Army Personals going for shooting practice from your camp at Malleswar to Mohi firing range in a 3 Ton. When you reached road junction, a few villagers with an injured person in a bullock cart stopped you and asked for help. The man who had been attacked by a Shark told you the incident. "I had been to the lighthouse Island for fishing and I overheard two smugglers discussing that a consignment of drugs was to reach the Island in a helicopter at 1100 hrs today. To divert the attention of the Coastal guard, they were planning to explode a bomb at the village school at 1130 hrs, where the coastal guard commander would be inaugurating the school's annual function. When they found out that I was listening, they tried to attack me, and I jumped into the sea and swam towards the shore. Unfortunately, a shark attacked me". At that time the NCO in charge tells you that he had forgotten to bring the targets for firing. 
The villagers further informed you that, the culvert had collapsed after they had passed through. Now time is 0930 hrs. As a group of brave young men, what will you do?
Scale 2CM = 1 KM
"""

# --- HELPER FUNCTIONS ---

def get_ppdt_image_path(set_number):
    """Returns the path to the PPDT image based on set number."""
    return os.path.join(PPDT_FOLDER_PATH, f"PPDT_{set_number}.jpg")

def get_audio_html(file_path):
    """Encodes an audio file to base64 for embedding in HTML, used for the stop sound."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f"""
            <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            return audio_html
    except FileNotFoundError:
        st.error(f"Error: Audio file not found at {file_path}. Cannot play stop sound.")
        return ""

def format_time(seconds):
    """Converts seconds into M:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:01}:{seconds:02}"

# --- INSTRUCTIONS CONTENT ---

PPDT_INSTRUCTIONS = """
### 📋 PPDT Instructions (Picture Perception and Discussion Test)

1.  **Viewing (30 seconds):** A hazy or clear picture will be displayed for **30 seconds**. Observe the picture carefully.
2.  **Perception & Writing (5 minutes):** After 30 seconds, the picture will disappear. You will have **5 minutes** to write the following:
    * **The central theme/action.**
    * **The total number of characters** observed, their **sex**, **age**, and **mood** (e.g., 3; 1M, 2F; 25-30; Happy).
    * **Your individual story** based on the picture, covering the past, present, and future action.
3.  **Discussion:** (Not implemented in this app, as it is a group activity).
"""

GPE_INSTRUCTIONS = """
### 🗺️ GPE Instructions (Group Planning Exercise)

1.  **Study the Map:** A map of an area will be displayed. Study the map, identifying key locations, distances, and resources (e.g., roads, river, bridges, hospitals, etc.).
2.  **Narration:** A problem statement or 'situation' will be given, detailing multiple concurrent problems and the resources available to your group.
3.  **Individual Solution (10 minutes):** You must mentally or on paper, formulate a **sequential, realistic, and time-bound solution** to all the problems.
4.  **Group Discussion (20 minutes):** (Not implemented in this app). The group decides on a common, best solution.
"""

# --- PAGE LAYOUT FUNCTIONS ---

def show_home_page():
    st.title("🪖🎖️⚔️ SSB Module App 48 MH Bn NCC")
    st.markdown("---")
    st.header("Please Select a Test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🖼️ PPDT (Picture Perception)", use_container_width=True):
            st.session_state.page = 'ppdt_sets'
            
    with col2:
        if st.button("🗺️ GPE (Group Planning Exercise)", use_container_width=True):
            st.session_state.page = 'gpe_instructions'
            
    st.markdown("""
    > **Note:** This is a mock-up. You must provide the actual images, maps, and sound files for full functionality.
    """)

# --- PPDT FUNCTIONS ---

def show_ppdt_sets():
    st.title("🖼️ PPDT: Select a Set")
    st.markdown("---")
    
    st.subheader("Choose the PPDT Set to Practice:")
    set_options = [f"Set {i}" for i in range(1, 6)]
    selected_set = st.selectbox("Select Set", set_options)

    if st.button(f"Start PPDT with {selected_set}", use_container_width=True):
        st.session_state.page = 'ppdt_instructions'
        st.session_state.ppdt_set = selected_set
        # Extract set number (1, 2, 3, etc.)
        st.session_state.ppdt_set_number = selected_set.split()[-1]

    if st.button("⬅️ Back to Home", key="back_ppdt_home"):
        st.session_state.page = 'home'

def show_ppdt_instructions():
    st.title(f"🖼️ PPDT Instructions ({st.session_state.ppdt_set})")
    st.markdown(PPDT_INSTRUCTIONS)
    
    st.warning(f"Total time for this test: {format_time(TOTAL_PPDT_TIME)}")
    
    if st.button("✅ Proceed to Test", use_container_width=True):
        st.session_state.page = 'ppdt_test'
        st.session_state.start_time = time.time()
        st.session_state.timer_running = True
        st.session_state.picture_visible = True
        st.rerun()

def show_ppdt_test():
    st.title(f"🖼️ PPDT: Story Writing ({st.session_state.ppdt_set})")
    
    if st.session_state.timer_running:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, TOTAL_PPDT_TIME - elapsed_time)
        
        # Check timer stages
        if remaining_time <= 0:
            st.session_state.timer_running = False
            st.session_state.picture_visible = False
            # Display stop sound
            audio_html = get_audio_html(STOP_SOUND_PATH)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
            st.error("⏰ **TIME UP! STOP WRITING.**")
            st.balloons()
            st.session_state.end_message = "Test Concluded."
            st.rerun()
            return
            
        elif remaining_time <= PPDT_WRITING_TIME:
            st.session_state.picture_visible = False
        
        # Layout: Picture viewing phase (30% left for timer, 70% right for picture)
        if st.session_state.picture_visible:
            col_timer, col_picture = st.columns([30, 70])
            
            with col_timer:
                st.markdown("### ⏱️ Timer")
                st.markdown("---")
                view_remaining = remaining_time - PPDT_WRITING_TIME
                st.metric("Viewing Time Remaining", format_time(view_remaining), delta=None)
                st.info("📸 **Picture Viewing Phase**\n\nObserve the picture carefully!")
                st.markdown("---")
                st.warning(f"Total Test Time: {format_time(TOTAL_PPDT_TIME)}")
                st.markdown(f"**Elapsed:** {format_time(elapsed_time)}")
            
            with col_picture:
                st.markdown("### 🖼️ PPDT Picture")
                # Get the correct image path based on set number
                image_path = get_ppdt_image_path(st.session_state.ppdt_set_number)
                
                if os.path.exists(image_path):
                    try:
                        # Provide a valid integer width so Streamlit accepts it.
                        st.image(image_path, caption=f"{st.session_state.ppdt_set}", width=700)
                    except Exception as e:
                        st.error(f"⚠️ Error loading image: {str(e)}")
                else:
                    st.error(f"⚠️ Picture not found at {image_path}")
                    st.info(f"Please ensure the file PPDT_{st.session_state.ppdt_set_number}.jpg exists in the '{PPDT_FOLDER_PATH}' folder.")
                    # Helpful diagnostic: show what files are in the ppdt folder
                    try:
                        entries = os.listdir(PPDT_FOLDER_PATH)
                        if entries:
                            st.write("Files found in the ppdt folder:")
                            for e in entries:
                                st.write("-", e)
                        else:
                            st.write("The ppdt folder is empty.")
                    except FileNotFoundError:
                        st.write(f"The folder '{PPDT_FOLDER_PATH}' does not exist. Create it and put PPDT_1.jpg, PPDT_2.jpg, ... inside.")
        
        else:
            # Story Writing Phase - No text areas, just timer display
            st.subheader(f"⏱️ Remaining Time: **{format_time(remaining_time)}**")
            st.info("✍️ **Story Writing Phase** - The picture has disappeared. Write your story on paper.")
            
            st.markdown("---")
            
            # Instructions for writing
            st.markdown("""
            ### 📝 Write on Your Paper:
            
            1. **Character Details**: Number of characters, Sex, Age, and Mood
               - Example: *3 characters; 2M, 1F; 25-30 years; Posititve or Negative or Neutral*
            
            2. **Central Theme/Action**: What is happening in the picture?
            
            3. **Your Story**: Write a complete story covering:
               - **Past**: What happened before
               - **Present**: What is happening now
               - **Future**: What will happen next
            """)
            
            st.markdown("---")
            st.markdown(f"**Time Elapsed:** {format_time(elapsed_time)} / {format_time(TOTAL_PPDT_TIME)}")
            
            # Progress bar
            progress = min(1.0, elapsed_time / TOTAL_PPDT_TIME)
            st.progress(progress)

        # Rerun to update timer every second
        time.sleep(1)
        st.rerun()

    else:
        st.subheader("✅ Test Completed")
        st.success(st.session_state.get('end_message', "PPDT Session Concluded."))
        
        # Play buzzer sound one more time on completion screen
        if st.session_state.get('end_message') == "Test Concluded.":
            audio_html = get_audio_html(STOP_SOUND_PATH)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start New PPDT", use_container_width=True):
                st.session_state.page = 'ppdt_sets'
                st.rerun()
        with col2:
            if st.button("⬅️ Back to Home", key="back_ppdt_end", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()

# --- GPE FUNCTIONS ---

def show_gpe_instructions():
    st.title("🗺️ GPE Instructions")
    st.markdown(GPE_INSTRUCTIONS)

    if st.button("✅ Proceed to GPE Map and Narration", use_container_width=True):
        st.session_state.page = 'gpe_test'
        st.session_state.hide_map = False
        st.session_state.hide_narration = False
        st.session_state.hide_problems = False
        st.rerun()

    if st.button("⬅️ Back to Home", key="back_gpe_home"):
        st.session_state.page = 'home'

def show_gpe_test():
    st.title("🗺️ GPE: Map and Problem Statement")
    st.warning("Start your Individual Solution Formulation Time (e.g., 10 minutes).")
    st.markdown("---")

    # Layout: 30% left for narration, 70% right for map
    col_narration, col_map = st.columns([30, 70])
    
    with col_narration:
        st.markdown("### 📋 Narration/Problem Statement")
        if not st.session_state.get('hide_narration', False):
            st.markdown(GPE_NARRATION)
        else:
            st.info("Narration is currently hidden.")
    
    with col_map:
        st.markdown("### 🗺️ GPE Map")
        if not st.session_state.get('hide_map', False):
            if os.path.exists(GPE_MAP_PATH):
                try:
                    st.image(GPE_MAP_PATH, caption="GPE Map (Study Area, Distances, and Resources)", width=700)
                except Exception as e:
                    st.error(f"⚠️ Error loading map image: {e}")
            else:
                st.error(f"⚠️ Map image not found at {GPE_MAP_PATH}. Please check file path.")
        else:
            st.info("Map is currently hidden.")
    
    st.markdown("---")
    
    # Toggle buttons below the content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Toggle Map Visibility", use_container_width=True):
            st.session_state.hide_map = not st.session_state.get('hide_map', False)
            st.rerun()
    
    with col2:
        if st.button("Toggle Narration Visibility", use_container_width=True):
            st.session_state.hide_narration = not st.session_state.get('hide_narration', False)
            st.rerun()
    
    with col3:
        if st.button("⬅️ Back to Home", key="back_gpe_end", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()


# --- MAIN APPLICATION LOGIC ---

def main():
    st.set_page_config(page_title="SSB Test Mock", layout="wide")
    
    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
        
    # Router
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'ppdt_sets':
        show_ppdt_sets()
    elif st.session_state.page == 'ppdt_instructions':
        show_ppdt_instructions()
    elif st.session_state.page == 'ppdt_test':
        show_ppdt_test()
    elif st.session_state.page == 'gpe_instructions':
        show_gpe_instructions()
    elif st.session_state.page == 'gpe_test':
        show_gpe_test()

if __name__ == "__main__":
    main()


