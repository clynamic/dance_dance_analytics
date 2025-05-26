from bs4 import BeautifulSoup, Tag
from flask import Response


def inject_subheads(response: Response) -> Response:
    if response.content_type.startswith("text/html"):
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, "html.parser")

        subheads = [tag for tag in soup.find_all("sub-head") if isinstance(tag, Tag)]
        if subheads:
            head = soup.find("head")
            if not isinstance(head, Tag):
                html_tag = soup.find("html")
                if isinstance(html_tag, Tag):
                    head = soup.new_tag("head")
                    html_tag.insert(0, head)
                else:
                    head = soup.new_tag("head")
                    soup.insert(0, head)

            for subhead in subheads:
                contents = subhead.decode_contents(formatter="html")
                new_soup = BeautifulSoup(contents, "html.parser")
                for element in new_soup.contents:
                    if isinstance(element, Tag):
                        head.append(element)
                subhead.decompose()

            response.set_data(str(soup))
    return response
