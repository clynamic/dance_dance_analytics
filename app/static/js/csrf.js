function getCSRFHeaders() {
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrf_token="))
    ?.split("=")[1];

  return {
    credentials: "include",
    headers: {
      "X-CSRF-Token": csrfToken,
    },
  };
}

function getCSRFFormData(formData) {
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrf_token="))
    ?.split("=")[1];

  if (csrfToken) {
    formData.append("csrf_token", csrfToken);
  }

  return formData;
}
