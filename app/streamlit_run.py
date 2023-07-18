import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# hashed_passwords = stauth.Hasher(['admin', 'def']).generate()
# input(hashed_passwords)
# Set wide=True
st.set_page_config(layout="wide")

with open('./cred.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    

    def crop_image(image, x, y, width, height):
        cropped_image = image.crop((x, y, x + width, y + height))
        return cropped_image

    menu_bar = option_menu(
        menu_title=st.session_state["name"],
        options = ["Menu", "Video", "Image", "xxxx", "logout"],
        # icons=[None, None, None, None, None],
        orientation="horizontal",
        default_index=0,
        menu_icon="house"
    )

    if menu_bar == "logout":
        col = st.columns(7)
        with col[1]:
            st.write("Press the button to logout.")
        with col[2]:
            authenticator.logout('Logout', 'main', key='unique_key')

    if menu_bar == "Menu":
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options = ["Status Tree", "Sites / Cameras", "Map View"],
                icons=["signpost-2", "webcam", "map"],
                default_index=0
            )

        if selected == "Status Tree":
            st.write("Config Page:")
            st.write("\nSelect: Alerts amd events via email")
            st.write("IP Camera RTSP Stream")
            st.write("\nSelect analytics:")
            st.write("Detect:")
            st.write("People")
            st.write("Cars")
            st.write("PPE")
            st.write("Counting")
            st.write("Weapons")
            st.write("Heatmap")
            st.write("Pose detection""")

        if selected == "Map View":
            # st.title(f"This is {selected} Page.")                
            penguins = sns.load_dataset("penguins")
            # st.dataframe(penguins[["species", "flipper_length_mm"]].sample(6))
            col_graphs = st.columns([.99,1])
            with col_graphs[0]:    
                # Create Figure beforehand
                fig = plt.figure(figsize=(9, 7))
                sns.histplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
                plt.title("Hello Penguins!")
                st.pyplot(fig)

            with col_graphs[1]:
            # Let Seaborn create the Figure
                sns.kdeplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
                plt.title("Hello again!")
                st.pyplot(plt.gcf())

                # Personally not a big fan of state based matplotlib
                # Pre-existing axes for the plot. Otherwise, call matplotlib.pyplot.gca() internally.
            # Methods that return a figure
            fig = sns.pairplot(penguins, hue="species")
            st.pyplot(fig)
            col_graphs = st.columns([.86,1])

            with col_graphs[0]:
                # Create ax and figure beforehand, most libs have this - object-oriented
                fig, ax = plt.subplots()
                sns.scatterplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", ax=ax)
                st.pyplot(fig)

            with col_graphs[1]:
                # Create Figure with multiple axes
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4))
                sns.histplot(
                    data=penguins, x="flipper_length_mm", hue="species", multiple="stack", ax=ax1
                )
                sns.kdeplot(
                    data=penguins, x="flipper_length_mm", hue="species", multiple="stack", ax=ax2
                )
                ax1.set_title("Hello Penguins!")
                ax2.set_title("Hello again!")

                fig.set_tight_layout(True)
                st.pyplot(fig)

    if menu_bar == "Video":
        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # Create sidebar
        list_dir= []
        selected_directory = script_directory
        if selected_directory:
            if os.path.exists(selected_directory):
                with os.scandir(selected_directory) as entries:
                    for entry in entries:
                        list_dir.append(entry.name)
            else:
                st.sidebar.write("Invalid directory path.")
        with st.sidebar:
            selected = option_menu(
                menu_title="Explorer",
                options = list_dir,
                # icons=["signpost-2", "webcam", "map"],
                default_index=0
            )
        video_file = open('video/star.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

    if menu_bar == "Image":
        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # Create sidebar
        list_dir= []
        selected_directory = script_directory
        if selected_directory:
            if os.path.exists(selected_directory):
                with os.scandir(selected_directory) as entries:
                    for entry in entries:
                        list_dir.append(entry.name)
            else:
                st.sidebar.write("Invalid directory path.")
        with st.sidebar:
            selected = option_menu(
                menu_title="Explorer",
                options = list_dir,
                # icons=["signpost-2", "webcam", "map"],
                default_index=0
            )
        sunset_imgs = [
            'images/senset_1.jpg',
            'images/senset_2.jpg',
            'images/senset_3.jpg',
            'images/senset_4.jpg',
            ]
        cols = st.columns([1,1,1], gap="small")
        with cols[0]:
            st.image(crop_image(Image.open(sunset_imgs[1]), int(0), int(0), int(6000), int(4000)), use_column_width=True)
            inner = st.columns(1)
            with inner[0]:
                st.image(crop_image(Image.open(sunset_imgs[2]), int(0), int(0), int(5000), int(1900)), width=910)
        with cols[1]:
            st.image(crop_image(Image.open(sunset_imgs[3]), int(0), int(0), int(5000), int(3300)), use_column_width=True)
        with cols[2]:
            st.image(Image.open(sunset_imgs[0]), use_column_width=True)

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
