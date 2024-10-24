# import streamlit as st
# import threading
# import time
# import json
# import os
# from users import user_data
# from send_email import send_email
# from dotenv import load_dotenv
# from utils_funcs import *
# from send_email_without_results import *

# load_dotenv()

# # Define a JSON file for persistent storage
# DATA_FILE = "data.json"

# # Load data from the JSON file
# def load_data():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, 'r') as f:
#             return json.load(f)
#     return {}

# # Save data to the JSON file
# def save_data(data):
#     with open(DATA_FILE, 'w') as f:
#         json.dump(data, f)

# # Remove user progress from JSON file
# def remove_user_progress(email):
#     progress = load_data()
#     if email in progress:
#         del progress[email]
#         save_data(progress)

# # Function to check user credentials
# def check_credentials(username, password):
#     return username in user_data and user_data[username] == password

# # Polling function to check progress from JSON
# def check_progress():
#     user_progress = load_data()
#     for email, data in user_progress.items():
#         if not data.get("task_complete", False):
#             return True  # Task is still running
#     return False  # No task is in progress

# def check_user_task(email):
#     user_progress = load_data()
#     if email in user_progress:
#         return user_progress[email].get("task_complete", False)
#     return None


# def main():
#     # Page 1: User Authentication
#     st.title("User Authentication")

#     if "username" not in st.session_state:
#         st.session_state["username"] = ""

#     if "password" not in st.session_state:
#         st.session_state["password"] = ""

#     st.session_state["username"] = st.text_input("Username", value=st.session_state["username"])
#     st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"])

#     if st.button("Login"):
#         if check_credentials(st.session_state["username"], st.session_state["password"]):
#             st.success("Login successful!")
#             st.session_state["authenticated"] = True
#         else:
#             st.error("Invalid username or password.")

#     if st.session_state.get("authenticated"):
#         show_email_input_page()


# def show_email_input_page():
#     st.title("Search Input Page")

#     user_progress = load_data()

#     if "email" not in st.session_state:
#         st.session_state["email"] = ""

#     if "keywords" not in st.session_state:
#         st.session_state["keywords"] = ""

#     if "selected_option" not in st.session_state:
#         st.session_state["selected_option"] = ""

#     if "task_in_progress" not in st.session_state:
#         st.session_state["task_in_progress"] = False

#     st.session_state["email"] = st.text_input("Enter your email", value=st.session_state["email"])

#     if not st.session_state["email"]:
#         st.warning("Please enter your email to proceed.")
#         return

#     # Block new requests if any task is still in progress
#     if check_progress():
#         st.warning("A task is already running. Please wait until it is complete.")
#         time.sleep(5)
#         st.rerun()

#     st.session_state["keywords"] = st.text_input("Enter keywords for search", value=st.session_state["keywords"])

#     dropdown_options = ["التجارة", "المقاولات", "التشغيل والصيانة والنظافة للمنشآت", "العقارات والأراضي", "الصناعة والتعدين والتدوير", "الغاز والمياه والطاقة",
#                          "المناجم والبترول والمحاجر", "الإعلام والنشر والتوزيع", "الاتصالات وتقنية المعلومات",
#                          "الزراعة والصيد", "الرعاية الصحية والنقاهة", "التعليم والتدريب",
#                          "التوظيف والاستقدام", "الأمن والسلامة", "النقل والبريد والتخزين",
#                          "المهن الاستشارية", "السياحة والمطاعم والفنادق وتنظيم المعارض",
#                          "المالية والتمويل والتأمين", "الخدمات الأخرى"]

#     st.session_state["selected_option"] = st.selectbox("النشاط الاساسي", dropdown_options,
#                                                        index=dropdown_options.index(st.session_state["selected_option"]) if st.session_state["selected_option"] else 0)

#     # Submit button
#     if st.button("Submit"):
#         user_progress[st.session_state["email"]] = {
#             "keywords": st.session_state["keywords"],
#             "selected_option": st.session_state["selected_option"],
#             "task_complete": False
#         }
#         save_data(user_progress)

#         # Start the background process in a thread
#         thread = threading.Thread(target=process_request, args=(st.session_state["email"], st.session_state["keywords"], st.session_state["selected_option"]))
#         thread.start()

#         # Show message
#         st.info("The process is running in the background. You will receive an email shortly.")

#     # Once the task is complete
#     task_status = check_user_task(st.session_state["email"])
#     if task_status:
#         st.success("Task completed successfully! You can now submit a new request.")


# def process_request(email, keywords, selected_option):

#     try:
#         time.sleep(5)  # Simulate processing time
#         to_addresses = [email]
#         subject = f"Search Results for {keywords}"
#         body = f"Keywords: {keywords}\nSelected Option: {selected_option}\nPlease find the attached results."

#         keywords = [keyword.strip() for keyword in keywords.split(',') if keyword.strip()]
#         main_activity = selected_option

#         result_files= get_terms_files(keywords, str(main_activity))  # Assume this is a defined function
#         agg_files()  # Assume this is a defined function

#         print("result_files: ", result_files)


#         if not result_files:  # Check if no Excel files were generated
#             # Update the email status in the JSON file
#             data = load_data()
#             data[email]["task_complete"] = True
#             data[email]["error_message"] = "No results found for your request."
#             save_data(data)

#             # Send an email indicating no results were found
#             no_results_subject = f"No Matches Found for {keywords}"
#             no_results_body = f"Keywords: {keywords}\nSelected Option: {selected_option}\nPlease Try Again With Different Keywords or Main Activity"
#             send_email_without_results(to_addresses, no_results_subject, no_results_body)
#             return  # Exit as there is no need to send results


#         send_email(to_addresses, subject, body)

#         # Update the email status in the JSON file
#         data=load_data()
#         data[email]["task_complete"]=True
#         save_data(data)

#     except Exception as e:
#         data= load_data()
#         data[email]["task_complete"]=False
#         data[email]["error_message"]="Failed to send message."
#         remove_user_progress(email)



# if __name__ == "__main__":
#     main()






# import streamlit as st
# import threading
# import time
# import json
# import os
# import pandas as pd
# from users import user_data
# from send_email import send_email
# from dotenv import load_dotenv
# from utils_funcs import *
# from send_email_without_results import *

# load_dotenv()

# # Define a JSON file for persistent storage
# DATA_FILE = "data.json"

# # Load data from the JSON file
# def load_data():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, 'r') as f:
#             return json.load(f)
#     return {}

# # Save data to the JSON file
# def save_data(data):
#     with open(DATA_FILE, 'w') as f:
#         json.dump(data, f)

# # Remove user progress from JSON file
# def remove_user_progress(email):
#     progress = load_data()
#     if email in progress:
#         del progress[email]
#         save_data(progress)

# # Function to check user credentials
# def check_credentials(username, password):
#     return username in user_data and user_data[username] == password

# # Polling function to check progress from JSON
# def check_progress():
#     user_progress = load_data()
#     # If the JSON file is empty or there are no tasks, return False
#     if not user_progress:
#         return False
#     for email, data in user_progress.items():
#         if not data.get("task_complete", False):
#             return True  # Task is still running
#     return False  # No task is in progress

# def check_user_task(email):
#     user_progress = load_data()
#     if email in user_progress:
#         return user_progress[email].get("task_complete", False)
#     return None

# def extract_keywords_from_file(uploaded_file):
#     try:
#         # Read the uploaded file
#         if uploaded_file.name.endswith('.csv'):
#             df = pd.read_csv(uploaded_file)
#         elif uploaded_file.name.endswith('.xlsx'):
#             df = pd.read_excel(uploaded_file)
#         else:
#             st.error("Unsupported file format. Please upload a CSV or Excel file.")
#             return []

#         # Ensure the 'keywords' column exists
#         if 'keywords' not in df.columns:
#             st.error("The uploaded file must contain a column named 'keywords'.")
#             return []

#         # Extract and return the keywords as a list
#         keywords = df['keywords'].dropna().tolist()
#         return keywords
#     except Exception as e:
#         st.error("Error reading file. Please ensure it is a valid CSV or Excel file.")
#         return []

# def main():
#     # Page 1: User Authentication
#     st.title("User Login")

#     if "username" not in st.session_state:
#         st.session_state["username"] = ""

#     if "password" not in st.session_state:
#         st.session_state["password"] = ""

#     st.session_state["username"] = st.text_input("Username", value=st.session_state["username"])
#     st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"])

#     if st.button("Login"):
#         if check_credentials(st.session_state["username"], st.session_state["password"]):
#             st.success("Login successful!")
#             st.session_state["authenticated"] = True
#         else:
#             st.error("Invalid username or password.")

#     if st.session_state.get("authenticated"):
#         show_email_input_page()

# def show_email_input_page():
#     st.title("Search Input")

#     user_progress = load_data()

#     if "email" not in st.session_state:
#         st.session_state["email"] = ""

#     if "keywords" not in st.session_state:
#         st.session_state["keywords"] = ""

#     if "selected_option" not in st.session_state:
#         st.session_state["selected_option"] = ""

#     if "task_in_progress" not in st.session_state:
#         st.session_state["task_in_progress"] = False

#     st.session_state["email"] = st.text_input(
#         "Please Enter your email(s) (comma separated).", value=st.session_state["email"]
#         )
    
#     if not st.session_state["email"]:
#         st.warning("Please enter your email to proceed.")
#         return

#     # Block new requests if any task is still in progress
#     if check_progress():
#         st.warning("A task is already running. Please wait until it is complete.")
#         time.sleep(5)
#         st.rerun()

#     # File upload for keywords
#     uploaded_file = st.file_uploader("Upload a file containing keywords (CSV or Excel with a column named 'keywords' that contains the keywords).", type=["csv", "xlsx"])
#     file_keywords = extract_keywords_from_file(uploaded_file) if uploaded_file else []

#     # Manual keyword entry
#     manual_keywords = st.text_input("Enter keywords for search (comma-separated)", value=st.session_state["keywords"])
#     manual_keywords_list = [kw.strip() for kw in manual_keywords.split(",") if kw.strip()]

#     # Combine keywords from both file and manual entry
#     all_keywords = list(set(file_keywords + manual_keywords_list))

#     dropdown_options = ["التجارة", "المقاولات", "التشغيل والصيانة والنظافة للمنشآت", "العقارات والأراضي", "الصناعة والتعدين والتدوير", "الغاز والمياه والطاقة",
#                          "المناجم والبترول والمحاجر", "الإعلام والنشر والتوزيع", "الاتصالات وتقنية المعلومات",
#                          "الزراعة والصيد", "الرعاية الصحية والنقاهة", "التعليم والتدريب",
#                          "التوظيف والاستقدام", "الأمن والسلامة", "النقل والبريد والتخزين",
#                          "المهن الاستشارية", "السياحة والمطاعم والفنادق وتنظيم المعارض",
#                          "المالية والتمويل والتأمين", "الخدمات الأخرى"]

#     st.session_state["selected_option"] = st.selectbox("النشاط الاساسي", dropdown_options,
#                                                        index=dropdown_options.index(st.session_state["selected_option"]) if st.session_state["selected_option"] else 0)
    
#     emails = [email.strip() for email in st.session_state["email"].split(",") if email.strip()]

#     # Submit button
#     if st.button("Submit"):
#         for email in emails:
#             user_progress[email] = {
#                 "keywords": all_keywords,
#                 "selected_option": st.session_state["selected_option"],
#                 "task_complete": False
#             }
#         save_data(user_progress)

#         # Start the background process in a thread
#         thread = threading.Thread(target=process_request, args=(emails, all_keywords, st.session_state["selected_option"]))
#         thread.start()

#         # Show message
#         st.info("The process is running in the background. You will receive an email shortly.")


#     # Once the task is complete
#     if emails:
#         task_status = check_user_task(emails[0])
#         if task_status:
#             st.success("Task completed successfully! You can now submit a new request.")

# def process_request(emails, keywords, selected_option):
#     try:
#         time.sleep(5)  # Simulate processing time
#         to_addresses = emails
#         subject = f"Search Results for {', '.join(keywords)}"
#         body = f"Keywords: {', '.join(keywords)}\nSelected Option: {selected_option}\nPlease find the attached results."

#         main_activity = selected_option

#         get_terms_files(keywords, str(main_activity))  # Assume this is a defined function
#         agg_files()  # Assume this is a defined function

#         today_date = pd.to_datetime('today').strftime('%Y-%m-%d')
#         file_name = f"tenders_{today_date}_filtered.csv"
        
#         if not os.path.isfile(file_name):
#             data = load_data()
#             for email in emails:
#                 data[email]["task_complete"] = True
#                 data[email]["error_message"] = "No results found for your request."
#             save_data(data)

#             no_results_subject = f"No Matches Found for {', '.join(keywords)}"
#             no_results_body = f"Keywords: {', '.join(keywords)}\nSelected Option: {selected_option}\nPlease Try Again With Different Keywords or Main Activity."
#             send_email_without_results(to_addresses, no_results_subject, no_results_body)
#             return

#         send_email(to_addresses, subject, body)

#         data = load_data()
#         for email in emails:
#             data[email]["task_complete"] = True
#         save_data(data)

#     except Exception as e:
#         data = load_data()
#         for email in emails:
#             data[email]["task_complete"] = False
#             data[email]["error_message"] = "Failed to send message."
#         remove_user_progress(email)

# if __name__ == "__main__":
#     main()






import streamlit as st
import os
import json
import pandas as pd
from dotenv import load_dotenv
from utils_funcs import get_terms_files, agg_files
from send_email import send_email
from send_email_without_results import send_email_without_results
from users import user_data
import time
load_dotenv()

# Define a JSON file for persistent storage
DATA_FILE = "data.json"

# Load data from the JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save data to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Remove user progress from JSON file
def remove_user_progress(email):
    progress = load_data()
    if email in progress:
        del progress[email]
        save_data(progress)

# Function to check user credentials
def check_credentials(username, password):
    return username in user_data and user_data[username] == password

# Polling function to check progress from JSON
def check_progress():
    user_progress = load_data()
    # If the JSON file is empty or there are no tasks, return False
    if not user_progress:
        return False
    for email, data in user_progress.items():
        if not data.get("task_complete", False):
            return True  # Task is still running
    return False  # No task is in progress

def check_user_task(email):
    user_progress = load_data()
    if email in user_progress:
        return user_progress[email].get("task_complete", False)
    return None

def extract_keywords_from_file(uploaded_file) -> list:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return []

        if 'keywords' not in df.columns:
            st.error("The uploaded file must contain a column named 'keywords'.")
            return []

        return df['keywords'].dropna().tolist()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return []

def show_email_input_page():
    st.title("Search Input")

    user_progress = load_data()

    if "email" not in st.session_state:
        st.session_state["email"] = ""

    if "keywords" not in st.session_state:
        st.session_state["keywords"] = ""

    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = ""

    if "task_in_progress" not in st.session_state:
        st.session_state["task_in_progress"] = False

    st.session_state["email"] = st.text_input(
        "Please Enter your email(s) (comma separated).", value=st.session_state["email"]
        )
    
    if not st.session_state["email"]:
        st.warning("Please enter your email to proceed.")
        return

    # Block new requests if any task is still in progress
    if check_progress():
        st.warning("A task is already running. Please wait until it is complete.")
        time.sleep(5)
        st.rerun()

    # File upload for keywords
    uploaded_file = st.file_uploader("Upload a file containing keywords (CSV or Excel with a column named 'keywords' that contains the keywords).", type=["csv", "xlsx"])
    file_keywords = extract_keywords_from_file(uploaded_file) if uploaded_file else []

    # Manual keyword entry
    manual_keywords = st.text_input("Enter keywords for search (comma-separated)", value=st.session_state["keywords"])
    manual_keywords_list = [kw.strip() for kw in manual_keywords.split(",") if kw.strip()]

    # Combine keywords from both file and manual entry
    all_keywords = list(set(file_keywords + manual_keywords_list))

    dropdown_options = ["التجارة", "المقاولات", "التشغيل والصيانة والنظافة للمنشآت", "العقارات والأراضي", "الصناعة والتعدين والتدوير", "الغاز والمياه والطاقة",
                         "المناجم والبترول والمحاجر", "الإعلام والنشر والتوزيع", "الاتصالات وتقنية المعلومات",
                         "الزراعة والصيد", "الرعاية الصحية والنقاهة", "التعليم والتدريب",
                         "التوظيف والاستقدام", "الأمن والسلامة", "النقل والبريد والتخزين",
                         "المهن الاستشارية", "السياحة والمطاعم والفنادق وتنظيم المعارض",
                         "المالية والتمويل والتأمين", "الخدمات الأخرى"]

    st.session_state["selected_option"] = st.selectbox("النشاط الاساسي", dropdown_options,
                                                       index=dropdown_options.index(st.session_state["selected_option"]) if st.session_state["selected_option"] else 0)
    
    emails = [email.strip() for email in st.session_state["email"].split(",") if email.strip()]

    # Submit button
    if st.button("Submit"):
        for email in emails:
            user_progress[email] = {
                "keywords": all_keywords,
                "selected_option": st.session_state["selected_option"],
                "task_complete": False
            }
        save_data(user_progress)
        
        st.info("The process is running in the background. You will receive an email shortly.")

        # Start the background process in a thread
        process_request(emails, all_keywords, st.session_state["selected_option"])



    # Once the task is complete
    if emails:
        task_status = check_user_task(emails[0])
        if task_status:
            st.success("Task completed successfully! You can now submit a new request.")

def process_request(emails, keywords, selected_option):
    try:
        time.sleep(5)  # Simulate processing time
        to_addresses = emails
        subject = f"Search Results for {', '.join(keywords)}"
        body = f"Keywords: {', '.join(keywords)}\nSelected Option: {selected_option}\nPlease find the attached results."

        main_activity = selected_option

        get_terms_files(keywords, str(main_activity))  # Assume this is a defined function
        agg_files()  # Assume this is a defined function

        today_date = pd.to_datetime('today').strftime('%Y-%m-%d')
        file_name = f"tenders_{today_date}_filtered.csv"
        
        if not os.path.isfile(file_name):
            data = load_data()
            for email in emails:
                data[email]["task_complete"] = True
                data[email]["error_message"] = "No results found for your request."
            save_data(data)

            no_results_subject = f"No Matches Found for {', '.join(keywords)}"
            no_results_body = f"Keywords: {', '.join(keywords)}\nSelected Option: {selected_option}\nPlease Try Again With Different Keywords or Main Activity."
            send_email_without_results(to_addresses, no_results_subject, no_results_body)
            return

        send_email(to_addresses, subject, body)

        data = load_data()
        for email in emails:
            data[email]["task_complete"] = True
        save_data(data)

    except Exception as e:
        data = load_data()
        for email in emails:
            data[email]["task_complete"] = False
            data[email]["error_message"] = "Failed to send message."
        remove_user_progress(email)

def main():
    st.title("User Login")

    # Initialize session state variables
    for key in ["username", "password"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    st.session_state["username"] = st.text_input("Username", value=st.session_state["username"])
    st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"])

    if st.button("Login"):
        if check_credentials(st.session_state["username"], st.session_state["password"]):
            st.success("Login successful!")
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password.")

    if st.session_state.get("authenticated"):
        show_email_input_page()

if __name__ == "__main__":
    main()











