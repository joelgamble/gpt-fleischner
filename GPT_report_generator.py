import openai as ai
import csv
import os
import random
import unicodedata

# config GPT API variables
ai.api_key = os.environ["OPENAI_API_KEY"]

#global variable
nodules = []

def generate_recom(text, mod):
    prompt = [
        {"role": "system", "content": "Act as a radiologist. Another radiologist wrote the following \"FINDINGS\" section from a radiology report. Your job is to make evidence and consensus-based recommendations for next steps. Be very concise. Be as succinct as possible. Ignore normal and clinically irrelevant findings. Don't regurgitate the Findings."},
        {"role": "user", "content": ("Make specific recommendations for the nodules mentioned in the following findings, based on the 2017 Fleischner Society Guidelines for Management of incidental Pulmonary Nodules Detected on CT images. If you are not told whether the patient is high risk or low risk, specify recommendations for both possibilities, where applicable.  Discuss ONLY the nodules. Ignore all other findings. Here are the FINDINGS: " + text)}
    ]

    response = ai.ChatCompletion.create(
        model = mod,
        messages = prompt,
        temperature = 0.1, #more focused, constrained responses
        max_tokens = 1000
    )    
    return response['choices'][0]['message']['content']

def generate_recom_fleischner(text, mod):
    prompt = [
        {"role": "system", "content": "Act as a radiologist. Another radiologist wrote the following \"FINDINGS\" section from a radiology report. Your job is to make evidence and consensus-based recommendations for next steps. Be very concise. Be as succinct as possible. Ignore normal and clinically irrelevant findings. Don't regurgitate the Findings."},
        {"role": "user", "content": ("These are the 2017 Fleischner Society Guidelines for Management of incidental Pulmonary Nodules Detected on CT images: " + fleischner_text + " BASED ON THOSE GUIDELINES, ANSWER THIS QUESTION: What is the recommended follow-up for the nodules mentioned in the following FINDINGS: " + text)}
    ]

    response = ai.ChatCompletion.create(
        model = mod,
        messages = prompt,
        temperature = 0.1, #more focused, constrained responses
        max_tokens = 1000
    )    
    return response['choices'][0]['message']['content']

def generate_recom_tuned(text, mod, fleischner_text):
    prompt = [
        {"role": "system", "content": "Base your answers on the 2017 Fleischner Society Guidelines: " + fleischner_text},
        {"role": "user", "content": ("What is the recommended follow-up for the nodules mentioned in the following FINDINGS: " + text)}
    ]

    response = ai.ChatCompletion.create(
        model = mod,
        messages = prompt,
        temperature = 0.1, #more focused, constrained responses
        max_tokens = 1000
    )    
    
    return response['choices'][0]['message']['content']

def gpt(text, mod) :
    prompt = [
        {"role": "system", "content": "Act as a radiologist who has complete knowledge of the medical literature and consensus guidelines."},
        {"role": "user", "content": (text)}
    ]

    response = ai.ChatCompletion.create(
        model = mod,
        messages = prompt,
        temperature = 0.1, #more focused, constrained responses
        max_tokens = 1500
    )    
    return response['choices'][0]['message']['content']

def importCSV(file_name, keys):
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip the header row

        for index, row in enumerate(csv_reader):
            dictionary = {key: value for key, value in zip(keys, row)}

            nodules.append(dictionary)

def load_fleischner(file_name):
    with open(file_name, 'r') as file:
        text = file.read()

    return text

def exportCSV(file_name, headers):

    with open(file_name, 'w') as file:
        csv_writer = csv.writer(file)
        
        csv_writer.writerow(headers) # header row

        for row in nodules:
            csv_writer.writerow(row.values() )  # write to csv file


def format_sentence(size, texture, location):
    sentence = str(size) + " mm " + texture + " nodule in the " + location + ". "
    return sentence 

def add_sent_report(sent):
    # the text of the CT chest report in which the nodule description is incorporated
    report = "Excellent opacification of the main pulmonary artery (HU 550). No pulmonary embolism. Mild bibasal atelectasis. No consolidation or septal thickening. " + sent + "No thoracic lymphadenopathy. No pleural or pericardial effusion. No visible coronary artery calcifications. Mild multilevel degenerative changes in the thoracic spine. Unchanged chronic wedge compression fracture of T12. Limited evaluation of the lower neck and upper abdomen is unremarkable."
    return report

def generate_reports(num_nodules):

    num_per_category = num_nodules
    numbers = ["single", "multiple"]
    locations = ["right upper lobe", "right middle lobe", "right lower lobe", "left upper lobe", "lingula", "left lower lobe"]

    for number in numbers:
        for x in range(num_per_category):
            
            i = 1
            if number == "multiple":
                i = random.randint(2, 5) # randomly pick how many nodules: 2-5 nodules

            ### solid ###
            texture = "solid"
            
            sentence = ""
            recom = ""
            for y in range(i):
                #solid nodules 3-5mm
                size = random.randint(3, 5)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            recom = "If low risk, no routine follow-up. If high risk, optional CT at 12 months."
            report = add_sent_report(sentence)
            nodules.append({"report": report, "sent": sentence, "Fleischner": recom, "GPT-3.5": "", "GPT-4": "", 
                            "GPT-3.5 Score": "", "GPT-3.5 Biopsy": "", "GPT-4 Score": "", "GPT-4 Biopsy": "",
                            "GPT-3.5 Fl": "", "GPT-4 Fl": ""})
                
            #solid nodules 6-8mm
            sentence = ""
            for y in range(i):
                size = random.randint(6, 8)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
            
            if i == 1:
                recom = "If low risk, CT at 6-12 months, then consider CT at 18-24 months. If high risk, CT at 6-12 months, then CT at 18-24 months"
            else:
                recom = "If low risk, CT at 3-6 months, then consider CT at 18-24 months. If high risk, CT at 3-6 months, then CT at 18-24 months"
            report = add_sent_report(sentence)
            nodules.append({"report": report, "sent": sentence, "Fleischner": recom, "GPT-3.5": "", "GPT-4": "", "GPT-3.5 Score": "", "GPT-3.5 Biopsy": "", "GPT-4 Score": "", "GPT-4 Biopsy": "",
                            "GPT-3.5 Fl": "", "GPT-4 Fl": ""})

            #solid nodules >8mm
            sentence = ""
            for y in range(i):
                size = random.randint(9, 12)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                recom = "Consider CT at 3 months, PET/CT, or tissue sampling."
            else:
                recom = "If low risk, CT at 3-6 months, then consider CT at 18-24 months. If high risk, CT at 3-6 months, then CT at 18-24 months"
            report = add_sent_report(sentence)
            nodules.append({"report": report, "sent": sentence, "Fleischner": recom, "GPT-3.5": "", "GPT-4": "", "GPT-3.5 Score": "", "GPT-3.5 Biopsy": "", "GPT-4 Score": "", "GPT-4 Biopsy": "",
                            "GPT-3.5 Fl": "", "GPT-4 Fl": ""})

            ### ground glass ###
            texture = "ground glass"
            
            #nodules 3-5mm
            sentence = ""
            for y in range(i):
                size = random.randint(3, 5)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                recom = "No routine follow-up."
            else:
                recom = "CT at 3-6 months. If stable, consider CT at 2 and 4 years."
            report = add_sent_report(sentence)
            nodules.append({"report": report, "sent": sentence, "Fleischner": recom, "GPT-3.5": "", "GPT-4": "", "GPT-3.5 Score": "", "GPT-3.5 Biopsy": "", "GPT-4 Score": "", "GPT-4 Biopsy": "",
                            "GPT-3.5 Fl": "", "GPT-4 Fl": ""})

            # nodules >=6mm
            sentence = ""
            for y in range(i):
                size = random.randint(6, 12)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                recom = "CT at 6-12 months to confirm persistence, then CT every 2 years until 5 years."
            else:
                recom = "CT at 3-6 months. Subsequent management based on the most suspicious nodule(s)."
            report = add_sent_report(sentence)
            nodules.append({"report": report, "sent": sentence, "Fleischner": recom, "GPT-3.5": "", "GPT-4": "", "GPT-3.5 Score": "", "GPT-3.5 Biopsy": "", "GPT-4 Score": "", "GPT-4 Biopsy": "",
                            "GPT-3.5 Fl": "", "GPT-4 Fl": ""})

            ### part solid ###
            texture = "part solid"

            # don't generate nodules 1-5mm, b/c per Fleischner, "In practice, part-solid nodules cannot be defined as such until >=6mm"
            # nodules >=6mm
            sentence = ""
            for y in range(i):
                size = random.randint(6, 12)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                recom = "CT at 3-6 months to confirm persistence. If unchanged and solid component remains <6 mm, annual CT should be performed for 5 years."
            else:
                recom = "CT at 3-6 months. Subsequent management based on the most suspicious nodule(s)."
            report = add_sent_report(sentence)
            nodules.append({"report": report, "sent": sentence, "Fleischner": recom, "GPT-3.5": "", "GPT-4": "", "GPT-3.5 Score": "", "GPT-3.5 Biopsy": "", "GPT-4 Score": "", "GPT-4 Biopsy": "",
                            "GPT-3.5 Fl": "", "GPT-4 Fl": ""})

    # print(str(len(nodules)))
    # for nod in nodules:
    #     print(nod)

def format_for_tuning(num_nodules, file, fleischner_text):

    # generate nodules
    num_per_category = num_nodules
    numbers = ["single", "multiple"]
    locations = ["right upper lobe", "right middle lobe", "right lower lobe", "left upper lobe", "lingula", "left lower lobe"]
    for number in numbers:
        for x in range(num_per_category):
            
            i = 1
            if number == "multiple":
                i = random.randint(2, 5) # randomly pick how many nodules: 2-5 nodules

            ### solid ###
            texture = "solid"
            
            sentence = ""
            recom = ""

            #solid nodules 3-5mm
            for y in range(i):
                size = random.randint(3, 5)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                logic = "STEP 1: Solid. STEP 2: Single (solitary). STEP 3: less than 6 mm. Therefore, follow-up is: "
            else:
                logic = "STEP 1: Solid. STEP 2: Multiple. STEP 3: less than 6 mm. Therefore, follow-up is: "
            
            recom = "If low risk, no routine follow-up. If high risk, optional CT at 12 months."
            report = add_sent_report(sentence)
            
            nodules.append({"report": report, "logic": logic, "sent": sentence, "Fleischner": recom})
                
            #solid nodules 6-8mm
            sentence = ""
            for y in range(i):
                size = random.randint(6, 8)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                logic = "STEP 1: Solid. STEP 2: Single (solitary). STEP 3: Between 6 and 8 mm (inclusive). Therefore, follow-up is: "
                recom = "If low risk, CT at 6-12 months, then consider CT at 18-24 months. If high risk, CT at 6-12 months, then CT at 18-24 months"
            else:
                logic = "STEP 1: Solid. STEP 2: Multiple. STEP 3: Between 6 and 8 mm (inclusive). Therefore, follow-up is: "
                recom = "If low risk, CT at 3-6 months, then consider CT at 18-24 months. If high risk, CT at 3-6 months, then CT at 18-24 months"
            
            report = add_sent_report(sentence)
            nodules.append({"report": report, "logic": logic, "sent": sentence, "Fleischner": recom})

            #solid nodules >8mm
            sentence = ""
            for y in range(i):
                size = random.randint(9, 12)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                logic = "STEP 1: Solid. STEP 2: Single (solitary). STEP 3: Greater than 8 mm. Therefore, follow-up is: "
                recom = "Consider CT at 3 months, PET/CT, or tissue sampling."
            else:
                logic = "STEP 1: Solid. STEP 2: Multiple. STEP 3: Greater than 8 mm. Therefore, follow-up is: "
                recom = "If low risk, CT at 3-6 months, then consider CT at 18-24 months. If high risk, CT at 3-6 months, then CT at 18-24 months"
            
            report = add_sent_report(sentence)
            nodules.append({"report": report, "logic": logic, "sent": sentence, "Fleischner": recom})

            ### ground glass ###
            texture = "ground glass"
            
            #nodules 3-5mm
            sentence = ""
            for y in range(i):
                size = random.randint(3, 5)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                logic = "STEP 1: Ground-glass. STEP 2: Single (solitary). STEP 3: Less than 6 mm. Therefore, follow-up is: "
                recom = "No routine follow-up."
            else:
                logic = "STEP 1: Ground-glass. STEP 2: Multiple. STEP 3: Less than 6 mm. Therefore, follow-up is: "
                recom = "CT at 3-6 months. If stable, consider CT at 2 and 4 years."
            report = add_sent_report(sentence)
            nodules.append({"report": report, "logic": logic, "sent": sentence, "Fleischner": recom})


            # nodules >=6mm
            sentence = ""
            for y in range(i):
                size = random.randint(6, 12)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                logic = "STEP 1: Ground-glass. STEP 2: Single (solitary). STEP 3: Greater than or equal to 6 mm. Therefore, follow-up is: "
                recom = "CT at 6-12 months to confirm persistence, then CT every 2 years until 5 years."
            else:
                logic = "STEP 1: Ground-glass. STEP 2: Multiple. STEP 3: Greater than or equal to 6 mm. Therefore, follow-up is: "
                recom = "CT at 3-6 months. Subsequent management based on the most suspicious nodule(s)."
            report = add_sent_report(sentence)
            nodules.append({"report": report, "logic": logic, "sent": sentence, "Fleischner": recom})


            ### part solid ###
            texture = "part solid"

            # don't generate nodules 1-5mm, b/c per Fleischner, "In practice, part-solid nodules cannot be defined as such until >=6mm"
            # nodules >=6mm
            sentence = ""
            for y in range(i):
                size = random.randint(6, 12)
                location = random.choice(locations)
                sentence = sentence + format_sentence(size, texture, location)
                
            if i == 1:
                logic = "STEP 1: Part-solid. STEP 2: Single (solitary). STEP 3: Greater than or equal to 6 mm. Therefore, follow-up is: "
                recom = "CT at 3-6 months to confirm persistence. If unchanged and solid component remains <6 mm, annual CT should be performed for 5 years."
            else:
                logic = "STEP 1: Part-solid. STEP 2: Multiple. STEP 3: Greater than or equal to 6 mm. Therefore, follow-up is: "
                recom = "CT at 3-6 months. Subsequent management based on the most suspicious nodule(s)."
            report = add_sent_report(sentence)
            nodules.append({"report": report, "logic": logic, "sent": sentence, "Fleischner": recom})

    # output nodules as JSON dictionary formatted for fine tuning
    with open(file, 'w') as f:
        for n in nodules:
            dict = {"messages": [{"role": "system", "content": "You are a radiologist. Be CONCISE. Be as succinct as possible. Ignore clinically irrelevant findings. Your job is to make evidence-based and consensus-based recommendations based on the imaging findings. For example, make recommendations for incidental lung nodules according to the 2017 Fleischner Society Guidelines for Management of Incidental Pulmonary Nodules Detected on CT images; those guidelines are: " + fleischner_text}, {"role": "user", "content": "Think logically and work through the Fleischner Guidelines following these steps: STEP 1: Is it solid, ground glass, or part solid? STEP 2: Is it a single nodule or are there multiple nodules? STEP 3: which size category does the nodule fit into?\n\nWhat is the recommended follow-up for following nodule(s): " + n["sent"] + " \n\n" + n["logic"]}, {"role": "assistant", "content": n["Fleischner"]}]} # attempt with CoT
       
            str_dict = str(dict)
            str_dict = str_dict.replace("'", "\"")
            f.write(str_dict + "\n")  # write to csv file

def fine_tune():
    # STEP 1 ##
    fleischner_text = load_fleischner("/Users/HOME_FOLDER/Desktop/fleischner-2.txt")
    format_for_tuning(50, "/Users/HOME_FOLDER/Desktop/Fleischner_nodules_tuning_27Aug2023-50.jsonl", fleischner_text)

    ## STEP 2 ##
    # response = ai.File.create(
    #     file=open("/Users/HOME_FOLDER/Desktop/Fleischner_nodules_tuning_27Aug2023-50.jsonl", "rb"),
    #     purpose='fine-tune'
    #     )
    # print(response)

    ## STEP 3 ##
    # response = ai.FineTuningJob.create(training_file="file-ID", model="gpt-3.5-turbo-0613", suffix="Fl2017-27Aug23-3")
    # print(response)

def main():

    ## Test GPT's knowledge of Fleischner Society guidelines
    # print(gpt("List the complete 2017 Fleischner Society recommendations for incidentally detected pulmonary nodules, which should be publically available on Radiopaedia.org. BASED ON THOSE GUIDELINES, ANSWER THIS QUESTION: What is the appropriate follow-up for a 11 mm solid nodule in the lingula?", "gpt-4"))

    ### fine tuning ###
    # fine_tune()

    ### Get Recommendation from GPT ### 
    # generate_reports(10)
    file_path = "/Users/HOME_FOLDER/Desktop/nodules.csv"
    headers = ["report", "sent", "Fleischner", "GPT_35_Tuned"]
    importCSV(file_path, headers)

    fleischner_text = load_fleischner("/Users/HOME_FOLDER/Desktop/fleischner.txt")

    for nodule in nodules:
        nodule["GPT-3.5"] = generate_recom(nodule["report"], "gpt-3.5-turbo")
        nodule["GPT-4"] = generate_recom(nodule["report"], "gpt-4")
        nodule["GPT-3.5 Fl"] = generate_recom_fleischner(nodule["report"], "gpt-3.5-turbo")
        nodule["GPT-4 Fl"] = generate_recom_fleischner(nodule["report"], "gpt-4")
        nodule["GPT_35_Tuned"] = generate_recom_tuned(nodule["report"], "ft:gpt-3.5-turbo-0613:personal:fl2017-27aug23-3:7rv6aq5b", fleischner_text)
    
    exportCSV(file_path, headers)    

main()
