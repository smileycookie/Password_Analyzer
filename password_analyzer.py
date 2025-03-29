# -*- coding: utf-8 -*-
#Created By: Ripunjay Singh
#Created ON: 18-March-2025
#Last Modified: 29- March-2025
#
# **Password Analyzer**


import re
import ipywidgets as widgets
from IPython.display import display, HTML

# List of common passwords
COMMON_PASSWORDS = {"password", "123456", "12345678", "qwerty", "abc123", "password1"}

# Function to check if the password contains sequential or repetitive characters
def is_sequential_or_repetitive(password):
    sequential_patterns = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(len(password) - 2):
        segment = password[i:i+3]
        if segment in sequential_patterns or segment[::-1] in sequential_patterns:
            return True
    if len(set(password)) == 1:  # Example: "aaaaa" or "11111"
        return True
    return False

# Function to check password strength
def check_password_strength(password, username="", email=""):
    username = username.lower()
    email = email.lower()
    password_lower = password.lower()

    strength_criteria = {
        "✅ Length (8+ chars)": len(password) >= 8,
        "✅ Uppercase Letter": any(char.isupper() for char in password),
        "✅ Lowercase Letter": any(char.islower() for char in password),
        "✅ Number": any(char.isdigit() for char in password),
        "✅ Special Character": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
        "✅ Not a Common Password": password_lower not in COMMON_PASSWORDS,
        "✅ No Sequential/Repetitive Chars": not is_sequential_or_repetitive(password),
        "✅ No Personal Info": username not in password_lower and email not in password_lower
    }

    strength_score = sum(strength_criteria.values())

    # Strength categories
    if strength_score == 8:
        strength = "🟢 Strong 🔒"
        color = "#28a745"
        emoji = "🟢💪"
        strength_meter.bar_style = "success"
    elif strength_score >= 5:
        strength = "🟠 Medium ⚠️"
        color = "#ffc107"
        emoji = "🟠🤔"
        strength_meter.bar_style = "warning"
    else:
        strength = "🔴 Weak 🚨"
        color = "#dc3545"
        emoji = "🔴😟"
        strength_meter.bar_style = "danger"

    strength_meter.value = strength_score
    strength_meter.description = f"Strength: {emoji}"  # Show emoji beside progress bar

    # HTML Styling for Bigger Output
    feedback_html = f"""
    <div style='font-size:18px; font-weight:bold; color:{color}; padding:10px; border-radius:10px; text-align:center;'>
        {strength}
    </div>
    <br>
    <div style='font-size:16px; padding:10px; border: 2px solid {color}; border-radius:10px;'>
    <ul>
    """
    for criteria, passed in strength_criteria.items():
        feedback_html += f"<li style='color:{'green' if passed else 'red'}; font-size:16px;'>{'✔' if passed else '✖'} {criteria}</li>"
    feedback_html += "</ul></div>"

    return HTML(feedback_html)

# Creating input widgets
password_input = widgets.Password(placeholder="Enter your password", description="🔑 Password:")
username_input = widgets.Text(placeholder="Optional", description="👤 Username:")
email_input = widgets.Text(placeholder="Optional", description="📧 Email:")
output = widgets.Output()

# Strength meter progress bar with emojis
strength_meter = widgets.IntProgress(value=0, min=0, max=8, description='Strength: 🟢')

# Password visibility toggle
def toggle_password_visibility(change):
    global password_input
    with output:
        output.clear_output()

    # Remove the old password field before creating a new one
    password_box.children = []

    if change.new:
        password_input = widgets.Text(value=password_input.value, placeholder="Enter your password", description="🔑 Password:")
    else:
        password_input = widgets.Password(value=password_input.value, placeholder="Enter your password", description="🔑 Password:")
    password_input.observe(on_password_change, names='value')
    password_box.children = [password_input]

toggle_button = widgets.ToggleButton(value=False, description="👁 Show Password")
toggle_button.observe(toggle_password_visibility, names='value')

# Function to update feedback
def on_password_change(change):
    with output:
        output.clear_output()
        display(check_password_strength(password_input.value, username_input.value, email_input.value))

# Attach event listeners
password_input.observe(on_password_change, names='value')
username_input.observe(on_password_change, names='value')
email_input.observe(on_password_change, names='value')

# Wrapper box for password input
password_box = widgets.VBox([password_input])

# Display UI
display(username_input, email_input, password_box, toggle_button, strength_meter, output)

