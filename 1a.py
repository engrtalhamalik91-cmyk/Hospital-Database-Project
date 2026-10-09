from datetime import datetime
import csv
import time
import os
import random

fieldnames = [
    "Patient ID", "Visit Time Stamp", "Name", "Age", "Gender", "Address", 
    "Contact Number", "Medical History", "Current Medications", "Allergies", 
    "Emergency Contact", "Insurance Provider", "Insurance Policy Number", 
    "Temperature", "Blood Pressure", "Blood Pressure Status", "Heart Rate",
    "Patient Status"  
]

patients = []

def load_patients_from_csv(filename="patients.csv"):
    global patients
    patients = [] 
    if os.path.exists(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Patient ID"] = str(row["Patient ID"]).strip()
                row["Age"] = int(row["Age"]) if row["Age"] else 0
                row["Temperature"] = float(row["Temperature"]) if row["Temperature"] else 0.0
                row["Heart Rate"] = int(row["Heart Rate"]) if row["Heart Rate"] else 0
                row["Patient Status"] = row.get("Patient Status", "OPD").strip()
                patients.append(row)
        print("Patient information loaded from CSV.")
    else:
        print("No existing patient information found. Starting fresh.")

def save_patients_to_csv(patients, filename="patients.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(patients)
    absolute_path = os.path.abspath(filename)
    print(f"Patient information saved to {absolute_path}")

def check_bp_status(systolic, diastolic):
    if systolic >= 140 or diastolic >= 90:
        return "High risk hypertension (consult a doctor)"
    elif systolic >= 130 or diastolic >= 80:
        return "Elevated blood pressure (monitor closely)"
    else:
        return "Normal blood pressure"

load_patients_from_csv()

while True:
    print("\n=========================================")
    print("      PATIENT INFORMATION SYSTEM         ")
    print("=========================================")
    print("1. Patient Check-in (New / Existing Patient)")
    print("2. Get Patient History by ID")
    print("3. View All Patients Records")
    print("4. Save to CSV")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        patient_ID = input("Enter Patient ID: ").strip()
        matching_patients = [p for p in patients if str(p["Patient ID"]).strip() == patient_ID]
        
        existing_patient = None
        if matching_patients:
            existing_patient = matching_patients[-1]
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
                    
            patient_information = {
                "Patient ID": patient_ID, "Visit Time Stamp": datetime.now().strftime("%d-%m-%Y : %I:%M:%S %p"),
                "Name": name, "Age": age, "Gender": gender, "Address": address, "Contact Number": contact_number,
                "Medical History": medical_history, "Current Medications": current_medications, "Allergies": allergies,
                "Emergency Contact": emergency_contact, "Insurance Provider": insurance_provider, "Insurance Policy Number": insurance_policy_number,
                "Temperature": temperature, "Blood Pressure": blood_pressure, "Blood Pressure Status": blood_pressure_status, "Heart Rate": heart_rate,
                "Patient Status": patient_status
            }
            patients.append(patient_information)
            print(f"\n[SUCCESS] OPD record for {name} saved successfully.")

        elif service_choice == "2":
            patient_status = "Admitted"
            print(f"\n[SUCCESS] {name} is now marked as ADMITTED.")
            print(f"[ONLINE] Connecting Live Patient Monitor for Bed...")
            print("Monitoring active... Records will auto-save EVERY 5 MINUTES for testing.")
            print("-> PRESS Ctrl+C TO DISCONNECT MONITOR AND GO BACK TO MAIN MENU <-")
            time.sleep(2)
            
            try:
                while True:
                    live_temp = round(random.uniform(97.5, 102.5), 1)
                    live_systolic = random.randint(115, 145)
                    live_diastolic = random.randint(75, 95)
                    live_bp = f"{live_systolic}/{live_diastolic}"
                    live_hr = random.randint(65, 105)
                    live_bp_status = check_bp_status(live_systolic, live_diastolic)
                    
                    print(f"\n--- [AUTO RECORD] {datetime.now().strftime('%I:%M:%S %p')} ---")
                    print(f"  Temp: {live_temp} °F | BP: {live_bp} | HR: {live_hr} BPM ({live_bp_status})")
                    
                    live_record = {
                        "Patient ID": patient_ID, "Visit Time Stamp": datetime.now().strftime("%d-%m-%Y : %I:%M:%S %p"),
                        "Name": name, "Age": age, "Gender": gender, "Address": address, "Contact Number": contact_number,
                        "Medical History": medical_history, "Current Medications": current_medications, "Allergies": allergies,
                        "Emergency Contact": emergency_contact, "Insurance Provider": insurance_provider, "Insurance Policy Number": insurance_policy_number,
                        "Temperature": live_temp, "Blood Pressure": live_bp, "Blood Pressure Status": live_bp_status, "Heart Rate": live_hr,
                        "Patient Status": patient_status
                    }
                    patients.append(live_record)
                    time.sleep(300) 
                    
            except KeyboardInterrupt:
                print("\n[DISCONNECTED] Patient monitor suspended. Returning to menu...")
        else:
            print("Invalid service selection. Returning to menu.")

    elif choice == "2":
        patient_ID = input("Enter Patient ID for History: ").strip()
        found_records = [p for p in patients if str(p["Patient ID"]).strip() == patient_ID]
        if found_records:
            print(f"\n--- History for ID: {patient_ID} ({len(found_records)} entries) ---")
            for idx, p in enumerate(found_records, 1):
                print(f"Entry #{idx} [{p['Visit Time Stamp']}] Status: {p['Patient Status']} | Temp: {p['Temperature']} | BP: {p['Blood Pressure']} | HR: {p['Heart Rate']}")
        else: print("Patient not found.")
            
    elif choice == "3":
        if len(patients) == 0: 
            print("No patients recorded yet.")
        else:
            print("\nAll Patients:")
            for patient in patients:
                print(patient)
                
    elif choice == "4":
        save_patients_to_csv(patients)
    elif choice == "5":
        print("System shutdown. Goodbye!")
        break
    else:
        print("Invalid choice.")
        time.sleep(2)
