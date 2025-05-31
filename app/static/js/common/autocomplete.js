customElements.define(
  "auto-complete",
  class Autocomplete extends HTMLElement {
    connectedCallback() {
      if (this.initialized) return;
      this.initialized = true;

      const input = this.previousElementSibling;
      if (!(input instanceof HTMLInputElement && input.name)) {
        console.warn('<auto-complete> must follow an <input name="...">');
        return;
      }

      this.classList.add("auto-complete");

      const dropdown = document.createElement("ul");
      dropdown.className = "ac-list";
      dropdown.hidden = true;
      this.appendChild(dropdown);

      const endpoint = this.getAttribute("endpoint");
      if (!endpoint) {
        console.warn('<auto-complete> requires an "endpoint" attribute');
        return;
      }

      const field = this.getAttribute("field") || input.name;
      const limit = this.getAttribute("limit") || 10;

      let debounceTimeout = null;
      let currentIndex = -1;

      const renderDropdown = (matches) => {
        dropdown.innerHTML = "";
        currentIndex = -1;

        if (!matches.length) {
          dropdown.hidden = true;
          return;
        }

        for (const match of matches) {
          const item = document.createElement("li");
          item.className = "ac-item";
          item.textContent = match;
          item.addEventListener("mousedown", () => {
            input.value = match;
            dropdown.hidden = true;
          });
          dropdown.appendChild(item);
        }

        dropdown.hidden = false;
      };

      const fetchMatches = async () => {
        const query = encodeURIComponent(input.value);
        try {
          const response = await fetch(
            `${endpoint}.json?field=${field}&query=${query}&limit=${limit}`
          );
          if (response.ok) {
            if (document.activeElement !== input) return;
            const data = await response.json();
            renderDropdown(data);
          }
        } catch (error) {
          console.error("Autocomplete fetch error:", error);
        }
      };

      const updateMatches = () => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(fetchMatches, 500);
      };

      input.addEventListener("focus", updateMatches);
      input.addEventListener("input", updateMatches);

      input.addEventListener("keydown", (e) => {
        const items = dropdown.querySelectorAll(".ac-item");
        if (!items.length) return;

        if (e.key === "ArrowDown") {
          e.preventDefault();
          currentIndex = (currentIndex + 1) % items.length;
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          currentIndex = currentIndex <= 0 ? -1 : currentIndex - 1;
        } else if (e.key === "Enter") {
          e.preventDefault();
          if (currentIndex >= 0)
            items[currentIndex].dispatchEvent(new Event("mousedown"));
          else dropdown.hidden = true;
        }

        items.forEach((item, i) =>
          item.classList.toggle("active", i === currentIndex)
        );
      });

      input.addEventListener("blur", () => {
        setTimeout(() => (dropdown.hidden = true), 100);
      });
    }
  }
);
