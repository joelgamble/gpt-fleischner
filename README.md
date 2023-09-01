# Recommendations for Incidental Lung Nodule Follow-up with GPT-3.5 and GPT-4  
Python code and files used for testing GPT-3.5 and GPT-4's lung nodule follow-up recommendations and for fine-tuning GPT-3.5.

This repository enables transparent review of the methodology of our recent research paper on the limitations of GPT in applying 2017 Fleischner Society guidelines. 

## Files

```bash
├── README.md
├── GPT_report_generator.py                              # Python application. Contains all the functions used to generate nodule descriptions and interact with the GPT API
├── static                                               # Static files for app
│   ├── fleischner.txt                                   # The Fleischner Guidelines as copied exactly from Radiopaedia.org, included in some prompts 
│   ├── Fleischner_nodules_tuning_27Aug2023-50.jsonl     # Prompts containing the nodules uesd to fine-tune a GPT-3.5 model
