
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import os
from core.admin_base import Admin
from core.member_base import Member
from core.book_model import Book

class SystemManagementMixin:
    def backup_data(self):
        print("\n" + "="*55)
        print(" "*15 + "SYSTEM DATA BACKUP")
        print("="*55 + "\n")
        
        # 1. Define the list of critical database files to backup
        files_to_backup = ["books.json", "members.json", "admins.json"]
        
        # 2. Ensure the backup directory exists, if not create it
        backup_dir = "Backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        # 3. Create a unique subfolder for the current backup using timestamp to avoid overwriting previous backups
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        current_backup_path = os.path.join(backup_dir, f"Backup_{timestamp}")
        
        try:
            os.makedirs(current_backup_path)
        except Exception as e:
            print(f"CRITICAL ERROR: Could not create backup folder. System Error: {e}")
            input("\nPress enter to go back...\n")
            return
            
        success_count = 0
        
        # 4. Copy each critical file to the backup folder, while checking for their existence and handling any errors gracefully
        for file in files_to_backup:
            # Check if the original file exists before attempting to copy. If it doesn't exist, log a warning and skip to the next file.
            if os.path.exists(file):
                try:
                    # Use copy2 to preserve file metadata (like modification time) in the backup
                    shutil.copy2(file, current_backup_path)
                    print(f"Successfully backed up: {file}")
                    success_count += 1
                except Exception as e:
                    print(f"Failed to backup '{file}'. Error: {e}")
            else:
                print(f"Warning: Original database '{file}' not found. Skipping...")
                
        # 5. Final Report
        print("-" * 55)
        if success_count > 0:
            print(f"SUCCESS! {success_count} files securely backed up to:\n{current_backup_path}")
        else:
            print("BACKUP FAILED: No files were backed up. Please check your main directory.")
            
        print("=" * 55)
        input("\nPress enter to go back...\n")

    def restore_data(self):
        print("\n" + "="*55)
        print(" "*15 + "SYSTEM DATA RESTORE")
        print("="*55 + "\n")
        
        backup_dir = "Backups"
        
        # 1. check if backup directory exists, if not then show error and return to dashboard
        if not os.path.exists(backup_dir):
            print("ERROR: No backups folder found! Create a backup first.")
            input("\nPress enter to go back...\n")
            return
            
        # 2. list all backup folders inside the backup directory, but only those that start with "Backup_" to ensure we are showing valid backup records
        # This also prevents any accidental files or folders from being displayed if they don't follow the backup naming convention
        backups = [f for f in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, f)) and f.startswith("Backup_")]
        
        if not backups:
            print("No backup records found inside the Backups folder.")
            input("\nPress enter to go back...\n")
            return
            
        # Sort the backup folders in reverse chronological order (newest first) based on their timestamp in the name, to make it easier for admins to find the most recent backup
        backups.sort(reverse=True)
        
        # 3. Show the list of available backups to the admin in a clear and organized manner, allowing them to choose which backup they want to restore from. Also provide an option to cancel and go back to the dashboard if they change their mind or realize they don't want to restore after all.
        print("Available Backups:")
        print("-" * 55)
        for idx, backup in enumerate(backups, 1):
            print(f"{idx}. {backup}")
        print("0. Cancel & Go Back")
        print("-" * 55)
        
        # Get the admin's choice for which backup to restore
        while True:
            try:
                choice = int(input("\nSelect backup number to restore: "))
            except ValueError:
                print("\nResponse must be in digits!\n")
                continue
                
            if choice == 0:
                return # Admin chose to cancel the restore operation and go back to the dashboard
            
            # Validate the choice to ensure it's within the range of available backups
            if choice < 1 or choice > len(backups):
                print(f"\nInvalid choice! Please select between 1 and {len(backups)}.\n")
                continue
            break
            
        # extract the selected backup folder name and construct its full path for the restore operation
        selected_backup = backups[choice - 1]
        backup_path = os.path.join(backup_dir, selected_backup)
        
        # Showing a critical warning message to the admin about the consequence of restoring data and asking for final confirmation before proceeding
        
        print("\n" + "⚠️"*20)
        print("🚨 CRITICAL WARNING 🚨")
        print("Restoring from a backup will overwrite the current system data and")
        print(f"system will be turned into '{selected_backup}' condition.")
        print(" This action cannot be undone!")
        print("⚠️"*20)
        
        confirm = input("\nAre you absolutely sure? Type 'YES' to proceed: ").strip().upper()
        
        if confirm != "YES":
            print("\nRestore operation canceled by admin safely.\n")
            input("Press enter to go back...\n")
            return
            
        # 4. Proceed with the restore operation by copying the backup files from the selected backup folder
        files_to_restore = ["books.json", "members.json", "admins.json"]
        success_count = 0
        
        for file in files_to_restore:
            source_file = os.path.join(backup_path, file)
            
            # Check if the source file exists in the backup folder
            if os.path.exists(source_file):
                try:
                    # Replacing the original file with the backup file using copy2 to preserve metadata.
                    shutil.copy2(source_file, file)
                    print(f"Restored successfully: {file}")
                    success_count += 1
                except Exception as e:
                    print(f"Failed to restore '{file}'. Error: {e}")
            else:
                print(f"Warning: '{file}' not found in this backup folder. Skipping...")
                
        # 5. Final Report
        print("-" * 55)
        if success_count > 0:
            print(f"SUCCESS! System has been restored to: {selected_backup}")
            
        else:
            print("RESTORE FAILED: No files were restored.")
            
        print("=" * 55)
        input("\nPress enter to go back...\n")
