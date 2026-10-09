from datetime import datetime
import pandas as pd 
import numpy as np
import os 
import time
import random

filename = "hospital_database.csv"

fieldname = [
    "Patient ID", "Visit Time Stamp", "Name", "Age", "Gender", "Address", 
    "Contact Number", "Medical History", "Current Medications", "Allergies", 
    "Emergency Contact", "Insurance Provider", "Insurance Policy Number", 
    "Temperature", "Blood Pressure", "Blood Pressure Status", "Heart Rate",
    "Patient Status"
]
def check_bp_status(systolic, diastolic):
    if systolic >= 140 or diastolic >= 90:
        return "High risk hypertension (consult a doctor)"
    elif systolic >= 130 or diastolic >= 80:
        return "Elevated blood pressure (monitor closely)"
    else:
        return "Normal blood pressure"
    
if os.path.exists(filename):
    
    df = pd.read_csv(filename)
    df['Patient ID'] = df['Patient ID'].astype(str).str.strip()
    print(f"[INFO] '{filename}' data has been loaded")
else:
    df = pd.DataFrame(columns=fieldname)
    print(f"[INFO] New Blank Table Has Been Formed")

while True:
    print("\n=========================================")
    print("      PATIENT INFORMATION SYSTEM (PD)    ")
    print("=========================================")
    print("1. Patient Check-in (New / Existing Patient)")
    print("2. Get Patient History by ID")
    print("3. View All Patients Records")
    print("4. Save Data to CSV")
    print("5. Full Exit (Without Saving)")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        patient_ID = input("Enter Patient ID: ").strip()
        
        matching_records = df[df['Patient ID'] == patient_ID]
        
        existing_patient = None
        if not matching_records.empty:
            existing_patient = matching_records.iloc[-1]
            print(f"\n[FOUND] Existing Patient Match! Name: {existing_patient['Name']}")
            name = existing_patient["Name"]
            age = existing_patient["Age"]
            gender = existing_patient["Gender"]
            address = existing_patient["Address"]
            contact_number = existing_patient["Contact Number"]
            medical_history = existing_patient["Medical History"]
            current_medications = existing_patient.get("Current Medications", "")
            allergies = existing_patient["Allergies"]
            emergency_contact = existing_patient["Emergency Contact"]
            insurance_provider = existing_patient["Insurance Provider"]
            insurance_policy_number = existing_patient["Insurance Policy Number"]
        else:
            print("\n[NEW] Patient ID not found. Registering as a new patient...")
            name = input("Enter patient's name: ").strip()
            while True:
                try:
                    age = int(input("Enter patient's age: "))
                    break
                except ValueError: print("Invalid input for age.")
            gender = input("Enter patient's gender: ").strip()
            address = input("Enter patient's address: ").strip()
            contact_number = input("Enter patient's contact number: ").strip()
            medical_history = input("Enter patient's medical history: ").strip()
            current_medications = input("Enter patient's current medications: ").strip()
            allergies = input("Enter patient's allergies: ").strip()
            emergency_contact = input("Enter patient's emergency contact: ").strip()
            insurance_provider = input("Enter patient's insurance provider: ").strip()
            insurance_policy_number = input("Enter patient's insurance policy number: ").strip()

        print("\nSelect Patient Service Type:")
        print("1. OPD (Manual Vitals Entry)")
        print("2. Admit Patient (Launches Auto Live Monitor)")
        service_choice = input("Enter selection (1 or 2): ").strip()
        print(f"\n[DEBUG] Service Type'{service_choice}' has been choosed.")
        if service_choice == "1":
            patient_status = "OPD"
            print(f"\n--- Entering Manual OPD Vitals for {name} ---")
            while True:
                try:
                    temperature = float(input("Enter temperature: "))
                    break
                except ValueError: print("Invalid temperature.")
                    
            while True:
                blood_pressure = input("Enter blood pressure (e.g., 120/80): ").strip()
                try:
                    bp_parts = blood_pressure.split('/')
                    systolic = int(bp_parts[0])
                    diastolic = int(bp_parts[1])
                    blood_pressure_status = check_bp_status(systolic, diastolic)
                    break
                except (ValueError, IndexError): print("Invalid BP format. Use systolic/diastolic (e.g., 120/80).")
                    
            while True:
                try:
                    heart_rate = int(input("Enter heart rate: "))
                    break
                except ValueError: print("Invalid heart rate.")
            
            
            new_record = pd.DataFrame([{
                "Patient ID": patient_ID, "Visit Time Stamp": datetime.now().strftime("%d-%m-%Y : %I:%M:%S %p"),
                "Name": name, "Age": age, "Gender": gender, "Address": address, "Contact Number": contact_number,
                "Medical History": medical_history, "Current Medications": current_medications, "Allergies": allergies,
                "Emergency Contact": emergency_contact, "Insurance Provider": insurance_provider, "Insurance Policy Number": insurance_policy_number,
                "Temperature": temperature, "Blood Pressure": blood_pressure, "Blood Pressure Status": blood_pressure_status, "Heart Rate": heart_rate,
                "Patient Status": patient_status
            }])
            
            df = pd.concat([df, new_record], ignore_index=True)
            print(f"\n[SUCCESS] OPD record for {name} saved to system memory.")

        elif service_choice == "2":
            
            patient_status = "Admitted"
            print(f"\n[SUCCESS] {name} is now marked as ADMITTED.")
            print(f"[ONLINE] Connecting Live Patient Monitor for Bed...")
            print("Monitoring active... Records will auto-save EVERY 5 MINUTES.")
            print("-> PRESS Ctrl+C TO DISCONNECT MONITOR AND GO BACK TO MAIN MENU <-")
            time.sleep(2)
            
            try:
                while True:
                    # Jadoo ki machine se real-time values generate ho rahi hain
                    live_temp = round(random.uniform(97.5, 102.5), 1)
                    live_systolic = random.randint(115, 145)
                    live_diastolic = random.randint(75, 95)
                    live_bp = f"{live_systolic}/{live_diastolic}"
                    live_hr = random.randint(65, 105)
                    live_bp_status = check_bp_status(live_systolic, live_diastolic)
                    
                    print(f"\n--- [AUTO RECORD] {datetime.now().strftime('%I:%M:%S %p')} ---")
                    print(f"  Temp: {live_temp} °F | BP: {live_bp} | HR: {live_hr} BPM ({live_bp_status})")
                    
                    live_record = pd.DataFrame([{
                        "Patient ID": patient_ID, "Visit Time Stamp": datetime.now().strftime("%d-%m-%Y : %I:%M:%S %p"),
                        "Name": name, "Age": age, "Gender": gender, "Address": address, "Contact Number": contact_number,
                        "Medical History": medical_history, "Current Medications": current_medications, "Allergies": allergies,
                        "Emergency Contact": emergency_contact, "Insurance Provider": insurance_provider, "Insurance Policy Number": insurance_policy_number,
                        "Temperature": live_temp, "Blood Pressure": live_bp, "Blood Pressure Status": live_bp_status, "Heart Rate": live_hr,
                        "Patient Status": patient_status
                    }])
                    
                    df = pd.concat([df, live_record], ignore_index=True)
                    
                    
                    time.sleep(300)
                    
            except KeyboardInterrupt:
                print("\n[DISCONNECTED] Patient monitor suspended. Returning to menu...")
        else:
            print("Invalid service selection. Returning to menu.")

    elif choice == "2":
        
        patient_ID = input("Enter Patient ID for History: ").strip()
        found_records = df[df['Patient ID'] == patient_ID]
        
        if not found_records.empty:
            print(f"\n--- History for ID: {patient_ID} ({len(found_records)} entries) ---")
            for idx, row in found_records.iterrows():
                print(f"[{row['Visit Time Stamp']}] Status: {row['Patient Status']} | Temp: {row['Temperature']} | BP: {row['Blood Pressure']} | HR: {row['Heart Rate']}")
        else: 
            print("Patient not found.")
            
    elif choice == "3":
        if df.empty: 
            print("\n[INFO] No patients recorded yet.")
        else:
            print("\n=========================================================================================")
            print("                                CURRENT HOSPITAL PATIENTS VITALS                         ")
            print("=========================================================================================")
            
           
            header_format = "{:<12} | {:<22} | {:<12} | {:<12} | {:<15} | {:<10} | {:<14}"
            
            print(header_format.format(
                "PATIENT ID", "VISIT TIMESTAMP", "NAME", "TEMPERATURE", "BLOOD PRESSURE", "HEART RATE", "STATUS"
            ))
            print("-" * 105)
            
            
            for idx, row in df.iterrows():
          
                p_id = str(row["Patient ID"])
                t_stamp = str(row["Visit Time Stamp"])
                p_name = str(row["Name"])
                p_temp = f"{row['Temperature']} °F"
                p_bp = str(row["Blood Pressure"])
                p_hr = f"{row['Heart Rate']} BPM"
                p_status = str(row["Patient Status"])
                

                print(header_format.format(p_id, t_stamp, p_name, p_temp, p_bp, p_hr, p_status))
                
            print("=========================================================================================")

    elif choice == "4":
        df.to_csv(filename, index=False, encoding='utf-8')
        excel_filename = "hospital_database.xlsx"
        
       
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Patients')
       
            workbook = writer.book
            worksheet = writer.sheets['Patients']
            
       
            from openpyxl.styles import Font
            bold_font = Font(bold=True)
            
       
            for col_num in range(1, len(df.columns) + 1):
                cell = worksheet.cell(row=1, column=col_num)
                cell.font = bold_font
                
       
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)
                
        print(f"[SUCCESS] All records have been permanently saved as a styled sheet: '{excel_filename}'")

        
    elif choice == "5":
        print("System shutdown. Goodbye!")
        break
        
    else:
        print("Invalid choice. Please choose between 1 and 5.")
        
    time.sleep(1)