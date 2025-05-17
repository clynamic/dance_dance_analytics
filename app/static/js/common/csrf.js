function getCSRFHeaders(contentType = "text/plain") {
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrf_token="))
    ?.split("=")[1];

  return {
    "Content-Type": contentType,
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
