import string
from copy import copy

import httpx
import asyncio
from stdlib_list import stdlib_list
import inflect

from chats.tool_code.text_shorteners import convert_md_to_text


class PyPIChecker:
    def __init__(self):
        self.base_url = "https://pypi.org/pypi"

    async def package_exists(self, package_name: str) -> bool:
        """Asynchronously check if a single package exists on PyPI."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{package_name}/json")
            return response.status_code == 200

    async def find_readme_from_github_for_package(self, package_name: str) -> str:
        """Find README.md from github for a package as found on pypi."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{package_name}/json")
            if response.status_code == 200:
                package_info = response.json()
                if "info" in package_info:
                    if "project_urls" in package_info["info"]:
                        if "Source" in package_info["info"]["project_urls"]:
                            source_url = package_info["info"]["project_urls"]["Source"]
                            if source_url.startswith("https://github.com"):
                                async with httpx.AsyncClient() as client:
                                    response = await client.get(f"{source_url}/blob/master/README.md")
                                    if response.status_code == 200:
                                        return response.text
                                    response = await client.get(f"{source_url}/blob/main/README.md")
                                    if response.status_code == 200:
                                        return response.text
                                    response = await client.get(f"{source_url}/blob/main/README")
                                    if response.status_code == 200:
                                        return response.text
            return ""

    async def describe_packages(self, package_list: list[str],
                                truncate_description_at: int = 1000) -> dict[str, dict[str, str]]:
        """Asynchronously get some descriptive info about packages."""
        async with httpx.AsyncClient() as client:
            tasks = [client.get(f"{self.base_url}/{package_name}/json") for package_name in package_list]
            responses = await asyncio.gather(*tasks)

            package_infos = dict(zip(package_list, [response.json() for response in responses]))
            for name, package_info in package_infos.items():
                if "message" in package_info and package_info["message"] == "Not Found":
                    continue
                if package_info["info"].get("description", "UNKNOWN") == "UNKNOWN":
                    # try to get readme from github
                    readme = await self.find_readme_from_github_for_package(name)
                    if readme:
                        package_info["info"]["description"] = readme

                description = convert_md_to_text(package_info["info"]["description"])[:truncate_description_at]
                info = {
                    "summary": package_info["info"]["summary"],
                    "description": description,
                    "keywords": package_info["info"]["keywords"],
                    "requires_python": package_info["info"]["requires_python"],
                }
                for key, value in copy(info).items():
                    if not value:
                        del info[key]
                package_infos[name] = info
            return package_infos

    async def packages_exist(self, package_list: list[str]):
        """Concurrently check if a list of packages exist on PyPI."""
        # query pypi
        tasks = [self.package_exists(pkg) for pkg in package_list]
        results = await asyncio.gather(*tasks)
        # add name back to results
        results_as_dict = dict(zip(package_list, results))
        return results_as_dict

    async def packages_or_variant_exist(self, package_list):
        """Concurrently check if a list of packages exist on PyPI."""
        # everything will be lower case
        package_list = [package_name.lower() for package_name in package_list]

        # need to track variants
        package_info = {
            name: {"variants": set(), "available": False} for name in package_list
        }

        engine = inflect.engine()

        depuctuated = set()
        plurals = set()
        singulars = set()
        for package_name in set(list(package_list)):
            # depuctuate
            cleaned = package_name.translate(str.maketrans('', '', string.punctuation))
            # Convert to lower case
            depuctuated.add(cleaned.lower())
            package_info[package_name]["variants"].add(cleaned.lower())

            # pluralize initial
            plural = engine.plural(package_name)
            if plural:
                plurals.add(plural)
                package_info[package_name]["variants"].add(plural)

            # pluralize cleaned
            plural = engine.plural(cleaned)
            if plural:
                plurals.add(plural)
                package_info[package_name]["variants"].add(plural)

            # singularize initial
            singular = engine.singular_noun(package_name)
            if singular:
                singulars.add(singular)
                package_info[package_name]["variants"].add(singular)

            # singularize cleaned
            singular = engine.singular_noun(cleaned)
            if singular:
                singulars.add(singular)
                package_info[package_name]["variants"].add(singular)

        # keep things unique
        expanded_list = set(package_list)
        expanded_list.update(depuctuated)
        expanded_list.update(singulars)
        expanded_list.update(plurals)

        # query pypi
        tasks = [self.package_exists(pkg) for pkg in expanded_list if isinstance(pkg, str)]
        results = await asyncio.gather(*tasks)
        # add name back to results
        results_as_dict = dict(zip(expanded_list, results))

        # If one variant is taken, name is not available.
        for package_name, info in package_info.items():
            # results shows if taken (not available) so we reverse it.
            availability_of_variants = [not results_as_dict[variant] for variant in info["variants"] if
                                        variant in results_as_dict]
            info["available"] = all(availability_of_variants)

        return package_info

    def check_if_in_any(self, package_name: str) -> bool:
        """Check if a package name is in a list of package names."""
        for version in ["2.6", "2.7", "3.2", "3.3",
                        "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]:
            if package_name in stdlib_list(version):
                return True
        return False

    def package_is_stdlib(self, package_list: list[str]) -> dict[str, bool]:
        """Check if a package is a standard library module."""
        results = {}
        for package in package_list:
            results[package] = self.check_if_in_any(package)
        return results

    def is_valid_string(self, package_name: str):
        """Check if a package name is a valid string."""
        invalid = ["requirements",
                   "requirements.txt",
                   "package_name",
                   "<package_name>",
                   "package-name",
                   "<package-name>"]

        return isinstance(package_name, str) and len(package_name) > 0 and not package_name in invalid


if __name__ == '__main__':
    # Asynchronous function to use the PyPIChecker

    async def main():
        checker = PyPIChecker()
        results = await checker.describe_packages(["faker", "names", "pandas"])
        print(results)


    async def check_exists():
        checker = PyPIChecker()
        to_check = [
            "mistune",
            "markdown2",
            "markdown",
            "mistletoe",
            "grip",
            "pymdown-extensions",
            "CommonMark",
            "MarkdownPP",
            "markdownify",
            "mistep"
        ]
        results = await checker.packages_exist(to_check)
        print(results)

        # package_list = ['numpy', 'friends', 'oxen', 'pandas', "goose", 'nonexistentpackage']


    async def variants():
        checker = PyPIChecker()
        package_list = [
            # "spellcheckbot",
            # "chatbot_spellcheck",
            # "prebot_spellcheck",
            "pychat_spellcheck",
            # "prompspell",
            # "chatcheck",
            # "chatspell",
            # "pycheckerbot",
            # "linguisticorrect",
            # "promptspell",
        ]
        results = await checker.packages_exist(package_list)
        print(results)
        for package, exists in results.items():
            print(f"Does {package} exist? {exists}")
        checker.check_if_in_any("nope_no_way_not_at_all")
        checker.check_if_in_any("io")


    # Run the asynchronous function
    asyncio.run(main())
