import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Set pad_token_id
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

def generate_learning_resources(dependency):
    resources = generator(f"You are a helpful assistant.I have a JavaScript dependency that I need to use in my project. Please provide a detailed example of how to use this dependency. Here are the specifics of the dependency I am using: Dependency Name: {dependency}", max_length=500)[0]['generated_text']
    resources = resources.split('\n')
    resources =  [resource for resource in resources if resource]
     # Define subfolder path
    subfolder_path = os.path.join('output', dependency)
     # Ensure subfolder exists
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    
    # Save to file
    # with open(os.path.join(subfolder_path, f'documnet.txt'), 'w') as f:
    #     for resource in resources:
    #         f.write(resource + '\n')
            
    return resources