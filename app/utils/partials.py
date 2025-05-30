from bs4 import BeautifulSoup, Tag
from flask import Response


def inject_partials(response: Response) -> Response:
    """
    Intercepts HTML responses and processes custom partial elements.

    This function was created to overcome the limitations of Jinja2 templating for
    building modular and component-based server-rendered applications.

    In traditional Jinja2:
      - Templates are linear, with explicit `{% block %}` markers to define where
        content goes.
      - There's no concept of self-contained components or dynamic injection of
        content like in modern frontend frameworks (e.g., Vue, React).
      - It's not possible for a partial template (like a sidebar) to dynamically inject
        styles, scripts, or other dependencies into the <head> or other parts of the page.

    This system introduces a custom "partial-" tag convention:
        - `<partial-<name>>` tags can be used in the HTML to define reusable components.
        - Each partial can specify a `location` attribute to control where its content
            is injected (e.g., `start` or `end` of the target element).
        - Partials can also have a `class` attribute to filter which target elements they
            should inject into, allowing for more flexible and modular design.

    The inject_partials function:
      1. Parses the full HTML response.
      2. Scans for all <partial-*> tags and groups them by their target tag name.
      3. For each partial, finds matching target tags (with optional class filter) and
         injects the partial's contents into them.
      4. Removes the partial elements from the final HTML.
      5. If any errors occur during processing, it falls back to returning the
         original unmodified HTML.

    This approach creates a mini server-side component system, enabling modular
    templates with clear dependency management, while remaining fully compatible
    with Flask and Jinja2.

    :param response: The Flask response object containing the HTML.
    :return: The modified (or original) Flask response.
    """
    if response.content_type.startswith("text/html"):
        try:
            html = response.get_data(as_text=True)
            soup = BeautifulSoup(html, "html.parser")

            partials_map = {}
            for tag in soup.find_all(True):
                if (
                    isinstance(tag, Tag)
                    and tag.name
                    and tag.name.startswith("partial-")
                ):
                    target_name = tag.name.replace("partial-", "")
                    partials_map.setdefault(target_name, []).append(tag)

            for target_name, partials in partials_map.items():
                hosts = [h for h in soup.find_all(target_name) if isinstance(h, Tag)]
                if not hosts:
                    print(
                        f"Warning: No target elements found for <partial-{target_name}>."
                    )
                    continue

                for partial in partials:
                    try:
                        partial_classes = partial.get("class", [])
                        if not isinstance(partial_classes, list):
                            partial_classes = [partial_classes]

                        contents = partial.decode_contents(formatter="html")
                        fragment = BeautifulSoup(contents, "html.parser")
                        elements = list(fragment.contents)
                        location = partial.get("location", "end")
                        once = partial.has_attr("once")

                        matched_hosts = hosts
                        if partial_classes:
                            matched_hosts = [
                                h
                                for h in hosts
                                if h.has_attr("class")
                                and any(
                                    cls in h.get("class", None)
                                    for cls in partial_classes
                                )
                            ]
                            if not matched_hosts:
                                print(
                                    f"Warning: No matching hosts found for partial {partial.name} with class {partial_classes}."
                                )
                                continue

                        for host in matched_hosts:
                            for el in elements:
                                el.extract()

                                if once:
                                    el_str = str(el)
                                    if any(
                                        str(existing) == el_str
                                        for existing in host.contents
                                    ):
                                        continue

                                if location == "start":
                                    host.insert(0, el)
                                else:
                                    host.append(el)
                        partial.decompose()

                    except Exception as e:
                        print(f"Warning: Failed to process partial {partial.name}: {e}")

            response.set_data(str(soup))

        except Exception as e:
            print(f"inject_partials: Exception encountered: {e}")
            return response

    return response
