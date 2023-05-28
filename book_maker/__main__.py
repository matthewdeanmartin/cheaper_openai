import yaml
with open("data.yml", encoding="utf-8") as data:
    toc = yaml.safe_load(data)

print(toc)
for section_info in toc:
    for section, chapters in section_info.items():
        for chapter in chapters:
            print(section, chapter)
