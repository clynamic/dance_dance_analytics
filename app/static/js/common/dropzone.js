function setupDropzone({
  dropArea,
  input,
  preview,
  placeholder,
  acceptedTypes,
}) {
  if (!dropArea || !input) return;

  const dragClass = "drag-hover";
  const hiddenClass = "hidden";

  function showPreview(file) {
    if (!preview || !file || (acceptedTypes && !file.type.match(acceptedTypes)))
      return;

    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.classList.remove(hiddenClass);
      if (placeholder) placeholder.classList.add(hiddenClass);
    };
    reader.readAsDataURL(file);
  }

  function clearPreview() {
    if (preview) preview.classList.add(hiddenClass);
    if (placeholder) placeholder.classList.remove(hiddenClass);
  }

  dropArea.addEventListener("dragenter", (e) => {
    e.preventDefault();
    dropArea.classList.add(dragClass);
  });

  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove(dragClass);
  });

  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove(dragClass);
    const file = e.dataTransfer.files[0];
    if (!file || (acceptedTypes && !file.type.match(acceptedTypes))) return;

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    input.files = dataTransfer.files;

    showPreview(file);
  });

  input.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      showPreview(file);
    } else {
      clearPreview();
    }
  });
}
