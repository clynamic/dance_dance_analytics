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

      const getOptions = () =>
        [...this.querySelectorAll("option")].map((o) => o.value);

      let currentIndex = -1;
      let currentMatches = [];

      const renderDropdown = (matches) => {
        dropdown.innerHTML = "";
        currentIndex = -1;
        currentMatches = matches;

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

      const updateMatches = () => {
        const value = input.value.toLowerCase();
        const matches = getOptions().filter((o) =>
          o.toLowerCase().includes(value)
        );
        renderDropdown(matches);
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
