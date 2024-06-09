import openai

openai.api_key = ''

def generate_learning_resources(dependency):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate learning resources for {dependency}.",
        max_tokens=100
    )
    resources = response.choices[0].text.strip().split('\n')
    return [resource for resource in resources if resource]
