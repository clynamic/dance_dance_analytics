function getSafeRedirect(defaultPath = "/") {
  const params = new URLSearchParams(window.location.search);
  const next = params.get("next");

  if (!next) return defaultPath;

  try {
    const targetUrl = new URL(next, window.location.origin);

    if (targetUrl.origin !== window.location.origin) {
      return defaultPath;
    }

    if (!targetUrl.pathname.startsWith("/")) {
      return defaultPath;
    }

    return targetUrl.pathname + targetUrl.search + targetUrl.hash;
  } catch {
    return defaultPath;
  }
}
