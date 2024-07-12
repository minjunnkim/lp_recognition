import tkinter as tk
from tkinter import messagebox

def show_profiles_screen(root, db, license_plate_text, profiles):
    profiles_window = tk.Toplevel(root)
    profiles_window.title("Profiles")

    def go_back():
        profiles_window.destroy()

    def create_profile():
        def save_profile():
            profile_name = profile_entry.get()
            if profile_name:
                # Add profile to the database
                db.profiles.update_one(
                    {'license_plate': license_plate_text},
                    {'$addToSet': {'profiles': profile_name}},
                    upsert=True
                )
                profiles.append(profile_name)
                profile_entry_window.destroy()
                profiles_window.destroy()
                show_profiles_screen(root, db, license_plate_text, profiles)
            else:
                messagebox.showerror("Error", "Profile name cannot be empty.")

        profile_entry_window = tk.Toplevel(profiles_window)
        profile_entry_window.title("Create Profile")
        tk.Label(profile_entry_window, text="Enter Profile Name:").pack(pady=10)
        profile_entry = tk.Entry(profile_entry_window)
        profile_entry.pack(pady=5)
        tk.Button(profile_entry_window, text="Save", command=save_profile).pack(pady=5)

    def remove_profile(profile):
        def confirm_remove():
            # Remove profile from the database
            db.profiles.update_one(
                {'license_plate': license_plate_text},
                {'$pull': {'profiles': profile}}
            )
            profiles.remove(profile)
            confirm_remove_window.destroy()
            profiles_window.destroy()
            show_profiles_screen(root, db, license_plate_text, profiles)

        confirm_remove_window = tk.Toplevel(profiles_window)
        confirm_remove_window.title("Confirm Remove")
        tk.Label(confirm_remove_window, text=f"Are you sure you want to remove profile '{profile}'?").pack(pady=10)
        tk.Button(confirm_remove_window, text="Yes", command=confirm_remove).pack(pady=5)
        tk.Button(confirm_remove_window, text="No", command=lambda: confirm_remove_window.destroy()).pack(pady=5)

    def select_profile(profile):
        messagebox.showinfo("Profile Selected", f"Selected profile: {profile}")

    tk.Label(profiles_window, text=f"Profiles for License Plate: {license_plate_text}").pack(pady=10)
    
    for profile in profiles:
        profile_frame = tk.Frame(profiles_window)
        profile_frame.pack(pady=5)
        tk.Label(profile_frame, text=profile).pack(side=tk.LEFT)
        tk.Button(profile_frame, text="Select", command=lambda p=profile: select_profile(p)).pack(side=tk.LEFT, padx=5)
        tk.Button(profile_frame, text="Remove", command=lambda p=profile: remove_profile(p)).pack(side=tk.RIGHT)

    tk.Button(profiles_window, text="Create Profile", command=create_profile).pack(pady=10)
    tk.Button(profiles_window, text="Back", command=go_back).pack(pady=5)