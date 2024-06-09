import json

def generate_documentation(repo_url, dependencies, dev_dependencies, scripts):
    with open('templates/report_template.md', 'r') as template_file:
        template = template_file.read()

    content = template.format(
        repo_url=repo_url,
        dependencies=json.dumps(dependencies, indent=4),
        dev_dependencies=json.dumps(dev_dependencies, indent=4),
        scripts=json.dumps(scripts, indent=4)
    )

    with open('project_documentation.md', 'w') as doc_file:
        doc_file.write(content)
